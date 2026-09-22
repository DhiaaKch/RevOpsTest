from app.db import get_orders, get_items_for_order

def list_orders_with_items(user_id: int) -> list[dict]:
    orders = get_orders(user_id)
    for order in orders:
        # PERF: N+1 — one query per order
        order["items"] = get_items_for_order(order["id"])
    return orders
