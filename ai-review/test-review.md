# Test Review — PR #13

## Missing / Suggested Tests (5)

### 🔴 No test verifies script tags in name are escaped in HTML output
- **File:** `app/api/render.py:1`
- **Scenario:** SECURITY

render_greeting interpolates user input directly into an HTML string. Without a test asserting that a <script> payload is neutralized, an XSS regression could ship undetected. This test would catch any future change that fails to escape HTML metacharacters.

```
# Scenario : A script tag in the name must not appear unescaped in the HTML output
# Why      : Catches XSS regressions where user input is reflected into HTML without escaping
def test_render_greeting_escapes_script_tag_in_name():
    # Arrange
    payload = "<script>alert('xss')</script>"

    # Act
    result = render_greeting(payload)

    # Assert
    assert "<script>" not in result
    assert "&lt;script&gt;" in result
```

### 🟠 No test verifies HTML attribute-breaking payloads are escaped
- **File:** `app/api/render.py:1`
- **Scenario:** SECURITY

An attacker can break out of the surrounding tag using quotes and angle brackets (e.g. "><img src=x onerror=alert(1)>). Without a test asserting these metacharacters are escaped, attribute-injection XSS can ship undetected.

```
# Scenario : Attribute-breaking payloads must be escaped so they cannot inject new tags
# Why      : Catches XSS via quote/angle-bracket breakout in reflected HTML
def test_render_greeting_escapes_attribute_breakout_payload():
    # Arrange
    payload = '\"><img src=x onerror=alert(1)>'

    # Act
    result = render_greeting(payload)

    # Assert
    assert "<img" not in result
    assert "onerror" not in result or "&quot;" in result
```

### 🟠 No happy-path test verifies normal names render correctly
- **File:** `app/api/render.py:1`
- **Scenario:** HAPPY_PATH

Without a baseline test for a plain alphanumeric name, a fix that over-escapes or breaks the greeting format could pass unnoticed. This test pins the expected output for benign input.

```
# Scenario : A plain alphanumeric name renders inside the greeting heading
# Why      : Catches regressions where escaping logic corrupts normal output
def test_render_greeting_renders_plain_name():
    # Arrange
    name = "Alice"

    # Act
    result = render_greeting(name)

    # Assert
    assert result == "<h1>Hello, Alice!</h1>"
```

### 🟡 No test covers empty string input for name
- **File:** `app/api/render.py:1`
- **Scenario:** EMPTY

An empty name is a common boundary input. Without a test, behavior for empty input is undefined and could produce malformed HTML or raise unexpectedly.

```
# Scenario : Empty string name produces a well-formed greeting with no injected content
# Why      : Catches crashes or malformed output on empty boundary input
def test_render_greeting_handles_empty_name():
    # Arrange
    name = ""

    # Act
    result = render_greeting(name)

    # Assert
    assert result == "<h1>Hello, !</h1>"
```

### 🟡 No test verifies ampersand and quote characters are escaped
- **File:** `app/api/render.py:1`
- **Scenario:** SECURITY

Ampersands and quotes are HTML metacharacters that must be escaped to prevent entity-injection and attribute breakout. Without a test, partial escaping implementations could pass CI.

```
# Scenario : Ampersand and quote characters in name are HTML-escaped
# Why      : Catches incomplete escaping that leaves HTML metacharacters intact
def test_render_greeting_escapes_ampersand_and_quotes():
    # Arrange
    name = 'Tom & "Jerry"'

    # Act
    result = render_greeting(name)

    # Assert
    assert "&amp;" in result
    assert "&quot;" in result
    assert ' & ' not in result
```

## Existing Test Issues (0)

No issues found in existing tests.