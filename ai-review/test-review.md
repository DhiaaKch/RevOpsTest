# Test Review — PR #5

## Missing / Suggested Tests (4)

### 🟡 No test for slugify_name happy path with normal names
- **File:** `app/utils/string_utils.py:1`
- **Scenario:** HAPPY_PATH

The new slugify_name helper has no tests at all. A regression in the strip/lower/replace chain (e.g. forgetting .lower() or using a space instead of underscore separator) would ship undetected. This verifies the core contract of the function.

```
# Scenario : slugify_name produces a lowercase underscore-joined slug for normal names
# Why      : Catches regressions in strip/lower/replace/join order that would break URL generation
def test_slugify_name_returns_lowercase_underscore_slug_for_normal_names():
    # Arrange
    first_name = "John"
    last_name = "Doe"

    # Act
    result = slugify_name(first_name, last_name)

    # Assert
    assert result == "john_doe"
```

### 🟡 No test for internal spaces being replaced with hyphens
- **File:** `app/utils/string_utils.py:1`
- **Scenario:** HAPPY_PATH

The function replaces internal spaces with hyphens before joining with an underscore. Without a test, a change to the replace target (e.g. replacing with underscore) would silently alter slug format and break downstream URL routing.

```
# Scenario : slugify_name replaces internal spaces with hyphens in each name part
# Why      : Catches accidental change of the replace target that would alter slug format
def test_slugify_name_replaces_internal_spaces_with_hyphens():
    # Arrange
    first_name = "Mary Jane"
    last_name = "Watson Parker"

    # Act
    result = slugify_name(first_name, last_name)

    # Assert
    assert result == "mary-jane_watson-parker"
```

### 🟡 No test for leading/trailing whitespace being stripped
- **File:** `app/utils/string_utils.py:1`
- **Scenario:** BOUNDARY

The function calls .strip() on both inputs. Without a test, removing the strip call would produce slugs with leading/trailing hyphens or spaces, breaking URL safety. This verifies the strip behavior explicitly.

```
# Scenario : slugify_name strips leading and trailing whitespace from both names
# Why      : Catches removal of .strip() that would leave whitespace in the slug
def test_slugify_name_strips_surrounding_whitespace():
    # Arrange
    first_name = "  Alice  "
    last_name = "\tSmith\n"

    # Act
    result = slugify_name(first_name, last_name)

    # Assert
    assert result == "alice_smith"
```

### 🔵 No test for empty string inputs
- **File:** `app/utils/string_utils.py:1`
- **Scenario:** EMPTY

Empty first or last name is a plausible input (e.g. optional last name). The function currently returns a slug with an empty segment. A test documents the actual behavior and catches accidental crashes or unexpected formatting changes.

```
# Scenario : slugify_name handles empty string inputs without raising
# Why      : Catches crashes or unexpected formatting when a name part is empty
def test_slugify_name_handles_empty_strings():
    # Arrange
    first_name = ""
    last_name = ""

    # Act
    result = slugify_name(first_name, last_name)

    # Assert
    assert result == "_"
```

## Existing Test Issues (0)

No issues found in existing tests.