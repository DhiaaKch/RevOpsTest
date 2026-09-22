def find_common(list_a: list[int], list_b: list[int]) -> list[int]:
    """Return elements that appear in both lists."""
    # PERF: O(n²) — nested scan instead of set-based lookup
    result = []
    for x in list_a:
        for y in list_b:
            if x == y:
                result.append(x)
                break
    return result
