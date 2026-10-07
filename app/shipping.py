def shipping_cost(weight_kg: float, express: bool = False) -> float:
    if weight_kg <= 0:
        raise ValueError("weight_kg must be positive")

    cost = 4.0 + 1.25 * weight_kg
    if express:
        cost += 8.0

    return round(cost, 2)
