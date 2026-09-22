def paginate(items: list, page: int, page_size: int) -> list:
    if page < 1:
        raise ValueError("page must be >= 1")
    start = (page - 1) * page_size
    # BUG: off-by-one: should be start + page_size, not start + page_size - 1
    end = start + page_size - 1
    return items[start:end]
