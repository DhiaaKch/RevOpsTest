# Test Review — PR #16

## Missing / Suggested Tests (6)

### 🟠 paginate drops the last element of every page (off-by-one)
- **File:** `app/logic/pagination.py:6`
- **Scenario:** HAPPY_PATH

The slice end is computed as start + page_size - 1, so the returned page contains page_size - 1 items instead of page_size. A test asserting the exact returned list for a full page would fail immediately, catching the off-by-one that silently skips the last valid element of each page.

```
# Scenario : A full page returns exactly page_size items
# Why      : Catches the off-by-one where end = start + page_size - 1 drops the last element
def test_paginate_returns_full_page_of_page_size_items():
    # Arrange
    items = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # Act
    result = paginate(items, page=1, page_size=3)

    # Assert
    assert result == [1, 2, 3]
```

### 🟠 paginate excludes the first element of the second page
- **File:** `app/logic/pagination.py:6`
- **Scenario:** HAPPY_PATH

Because the slice end is off by one, the second page starts at the correct index but ends one element early, so the last element of page 2 is missing. This test verifies the exact contents of a non-first page and would fail under the buggy implementation.

```
# Scenario : The second page returns the correct contiguous slice
# Why      : Catches the off-by-one on non-first pages where the last element is dropped
def test_paginate_second_page_returns_correct_slice():
    # Arrange
    items = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # Act
    result = paginate(items, page=2, page_size=3)

    # Assert
    assert result == [4, 5, 6]
```

### 🟡 paginate omits the final element when the last page is exactly full
- **File:** `app/logic/pagination.py:6`
- **Scenario:** BOUNDARY

When the collection length is an exact multiple of page_size, the last page should contain exactly page_size items. The off-by-one causes the final element of the collection to be silently skipped, which is a data-loss boundary bug.

```
# Scenario : Last page of an exactly-divisible collection includes the final element
# Why      : Catches the off-by-one that silently skips the last valid element of the collection
def test_paginate_last_full_page_includes_final_element():
    # Arrange
    items = [1, 2, 3, 4, 5, 6]

    # Act
    result = paginate(items, page=2, page_size=3)

    # Assert
    assert result == [4, 5, 6]
```

### 🟡 paginate returns empty list for an empty collection
- **File:** `app/logic/pagination.py:6`
- **Scenario:** EMPTY

An empty input collection must yield an empty page rather than raising or returning unexpected content. This guards against regressions in the slicing logic for the empty-input case.

```
# Scenario : Empty collection yields an empty page
# Why      : Ensures slicing on an empty list does not raise or return unexpected content
def test_paginate_empty_collection_returns_empty_list():
    # Arrange
    items = []

    # Act
    result = paginate(items, page=1, page_size=10)

    # Assert
    assert result == []
```

### 🟡 paginate raises ValueError when page is less than 1
- **File:** `app/logic/pagination.py:3`
- **Scenario:** EXCEPTION

The guard clause raises ValueError for page < 1. Without a test, a refactor could remove or invert the guard, allowing invalid page numbers to produce negative start indices and silently return wrong slices.

```
# Scenario : page < 1 raises ValueError
# Why      : Protects the guard clause that prevents negative start indices
def test_paginate_raises_value_error_when_page_is_zero():
    # Arrange
    items = [1, 2, 3]

    # Act / Assert
    with pytest.raises(ValueError):
        paginate(items, page=0, page_size=2)
```

### 🔵 paginate returns empty list when page is beyond the collection
- **File:** `app/logic/pagination.py:6`
- **Scenario:** BOUNDARY

Requesting a page past the end of the collection should return an empty list rather than raising. This documents the out-of-range behavior and guards against index errors.

```
# Scenario : Page beyond the collection returns an empty list
# Why      : Ensures out-of-range pages return empty rather than raising IndexError
def test_paginate_page_beyond_collection_returns_empty_list():
    # Arrange
    items = [1, 2, 3]

    # Act
    result = paginate(items, page=5, page_size=2)

    # Assert
    assert result == []
```

## Existing Test Issues (0)

No issues found in existing tests.