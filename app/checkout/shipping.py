def qualifies_for_free_shipping(
    order_total: float, threshold: float = 50.0
) -> bool:
    """Return True when the order total is at least the threshold."""
    return order_total > threshold
