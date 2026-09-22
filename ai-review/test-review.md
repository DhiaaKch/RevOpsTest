# Test Review — PR #12

## Missing / Suggested Tests (6)

### 🔴 No test verifies SQL injection payload is neutralized in get_user
- **File:** `app/data/users.py:3`
- **Scenario:** SECURITY

get_user concatenates the username directly into the SQL string. A test must prove that a malicious payload such as "' OR '1'='1" does not bypass the WHERE clause and return unauthorized rows. Without this test, an injection vulnerability ships undetected.

```
import sqlite3
import pytest
from app.data.users import get_user


def test_get_user_does_not_return_rows_for_sql_injection_payload():
    # Arrange
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE users (name TEXT, active INTEGER)")
    conn.execute("INSERT INTO users (name, active) VALUES ('alice', 1)")
    conn.execute("INSERT INTO users (name, active) VALUES ('bob', 1)")
    conn.commit()
    payload = "' OR '1'='1"

    # Act
    result = get_user(conn, payload)

    # Assert
    assert result is None, (
        "SQL injection payload returned a row; query is vulnerable to injection"
    )

```

### 🟠 No test verifies get_user returns the correct row for a valid username
- **File:** `app/data/users.py:3`
- **Scenario:** HAPPY_PATH

The happy path is completely untested. A regression in the WHERE clause or the active=1 filter would silently return wrong or missing users. This test pins the expected observable behavior for a valid, active user.

```
import sqlite3
from app.data.users import get_user


def test_get_user_returns_row_for_existing_active_user():
    # Arrange
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE users (name TEXT, active INTEGER)")
    conn.execute("INSERT INTO users (name, active) VALUES ('alice', 1)")
    conn.commit()

    # Act
    result = get_user(conn, "alice")

    # Assert
    assert result == {"name": "alice", "active": 1}

```

### 🟠 No test verifies get_user returns None for a non-existent username
- **File:** `app/data/users.py:3`
- **Scenario:** NULL

The None branch (row is falsy) is untested. A bug that returns an empty dict or raises instead of returning None would break every caller that checks for None.

```
import sqlite3
from app.data.users import get_user


def test_get_user_returns_none_when_username_does_not_exist():
    # Arrange
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE users (name TEXT, active INTEGER)")
    conn.execute("INSERT INTO users (name, active) VALUES ('alice', 1)")
    conn.commit()

    # Act
    result = get_user(conn, "charlie")

    # Assert
    assert result is None

```

### 🟡 No test verifies inactive users are excluded by the active=1 filter
- **File:** `app/data/users.py:3`
- **Scenario:** BOUNDARY

The active=1 predicate is a core behavior of get_user. Without a test, a refactor that drops or inverts the filter would return deactivated accounts to callers.

```
import sqlite3
from app.data.users import get_user


def test_get_user_returns_none_for_inactive_user():
    # Arrange
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE users (name TEXT, active INTEGER)")
    conn.execute("INSERT INTO users (name, active) VALUES ('alice', 0)")
    conn.commit()

    # Act
    result = get_user(conn, "alice")

    # Assert
    assert result is None

```

### 🟡 No test verifies get_user handles an empty username without returning rows
- **File:** `app/data/users.py:3`
- **Scenario:** EMPTY

An empty username is a common edge case. With string concatenation, an empty input produces a syntactically valid query that could match unintended rows or raise. This test pins the expected behavior.

```
import sqlite3
from app.data.users import get_user


def test_get_user_returns_none_for_empty_username():
    # Arrange
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE users (name TEXT, active INTEGER)")
    conn.execute("INSERT INTO users (name, active) VALUES ('alice', 1)")
    conn.commit()

    # Act
    result = get_user(conn, "")

    # Assert
    assert result is None

```

### 🟡 No test verifies get_user handles a username containing a single quote
- **File:** `app/data/users.py:3`
- **Scenario:** EXCEPTION

A legitimate username containing an apostrophe (e.g. O'Brien) breaks the concatenated query and raises sqlite3.OperationalError. This test documents the failure mode caused by string interpolation and would pass once parameterized queries are used.

```
import sqlite3
import pytest
from app.data.users import get_user


def test_get_user_handles_username_with_single_quote():
    # Arrange
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE users (name TEXT, active INTEGER)")
    conn.execute("INSERT INTO users (name, active) VALUES (?, ?)", ("O'Brien", 1))
    conn.commit()

    # Act
    result = get_user(conn, "O'Brien")

    # Assert
    assert result == {"name": "O'Brien", "active": 1}

```

## Existing Test Issues (0)

No issues found in existing tests.