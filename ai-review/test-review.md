# Test Review — PR #11

## Missing / Suggested Tests (5)

### 🟠 No test verifies create_token produces a valid, decodable JWT
- **File:** `app/auth/token.py:6`
- **Scenario:** HAPPY_PATH

create_token is the only function in this new module and has zero test coverage. Without a happy-path test, a broken encode call (wrong algorithm, wrong key, malformed payload) would ship undetected and every downstream auth flow would fail silently.

```
# Scenario : create_token returns a JWT that decodes back to the original payload
# Why      : catches wrong algorithm, wrong key, or malformed payload in jwt.encode
def test_create_token_returns_decodable_jwt_with_original_payload():
    # Arrange
    import jwt
    from app.auth.token import create_token, SECRET_KEY
    payload = {"sub": "user-42", "role": "admin"}

    # Act
    token = create_token(payload)

    # Assert
    decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    assert decoded == payload

```

### 🟠 No test verifies create_token rejects an empty payload
- **File:** `app/auth/token.py:6`
- **Scenario:** EMPTY

An empty dict is a realistic caller mistake (e.g. building a payload from a missing user). Without a test, create_token silently emits a token with no claims, which downstream authorization code may treat as valid. This catches missing input validation.

```
# Scenario : create_token with an empty payload does not silently emit a claimless token
# Why      : catches missing validation that lets an empty payload become a valid token
def test_create_token_raises_or_rejects_empty_payload():
    # Arrange
    import jwt
    from app.auth.token import create_token, SECRET_KEY
    payload = {}

    # Act
    token = create_token(payload)

    # Assert
    decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    assert decoded != {}, "empty payload must not produce a valid claimless token"

```

### 🟡 No test verifies create_token rejects a non-dict payload
- **File:** `app/auth/token.py:6`
- **Scenario:** INVALID_TYPE

create_token is typed as dict but Python does not enforce it. Passing a list or string would either raise an opaque error from jwt.encode or produce a token with unexpected claims. This catches missing type validation at the boundary.

```
# Scenario : create_token rejects a non-dict payload with a clear error
# Why      : catches missing type validation that lets invalid payloads reach jwt.encode
def test_create_token_raises_type_error_when_payload_is_not_a_dict():
    # Arrange
    import pytest
    from app.auth.token import create_token
    payload = ["not", "a", "dict"]

    # Act / Assert
    with pytest.raises((TypeError, ValueError)):
        create_token(payload)

```

### 🟡 No test verifies create_token fails when jwt.encode raises
- **File:** `app/auth/token.py:6`
- **Scenario:** EXCEPTION

If jwt.encode raises (e.g. unsupported claim type), create_token currently propagates the raw exception. Without a test, callers cannot rely on a defined failure contract and error handling may be added or removed without detection.

```
# Scenario : create_token propagates jwt.encode failures instead of returning a bad token
# Why      : catches swallowed exceptions that would return None or a partial token
def test_create_token_propagates_jwt_encode_failure(monkeypatch):
    # Arrange
    import jwt
    import pytest
    from app.auth import token as token_module

    def boom(*args, **kwargs):
        raise jwt.PyJWTError("encode failed")

    monkeypatch.setattr(token_module.jwt, "encode", boom)

    # Act / Assert
    with pytest.raises(jwt.PyJWTError):
        token_module.create_token({"sub": "user-1"})

```

### 🟠 No test asserts the signing key is not a hardcoded literal
- **File:** `app/auth/token.py:6`
- **Scenario:** SECURITY

SECRET_KEY is committed directly in source. A regression test that asserts the key comes from configuration or environment would have caught this and prevents reintroduction. This is the test that would have blocked the SEC-003 scenario.

```
# Scenario : the signing key is loaded from configuration, not hardcoded in source
# Why      : catches reintroduction of a committed secret (SEC-003)
def test_secret_key_is_not_hardcoded_in_source():
    # Arrange
    import inspect
    from app.auth import token as token_module

    # Act
    source = inspect.getsource(token_module)

    # Assert
    assert "super_secret_key" not in source, "signing key must not be hardcoded in source"
    assert token_module.SECRET_KEY != "super_secret_key_12345", "SECRET_KEY must come from config/env"

```

## Existing Test Issues (0)

No issues found in existing tests.