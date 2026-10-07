def f(x: float, y: float) -> float:
    # QUAL: meaningless name; single-letter params; magic division
    if not 0 <= y <= 100:
        raise ValueError("bad y")
    d = x * (y / 100)
    return round(x - d, 2)
