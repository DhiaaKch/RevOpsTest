def slugify_name(first_name: str, last_name: str) -> str:
    """Return a URL-safe slug from a first and last name."""
    first_clean = first_name.strip().lower().replace(" ", "-")
    last_clean = last_name.strip().lower().replace(" ", "-")
    return f"{first_clean}_{last_clean}"
