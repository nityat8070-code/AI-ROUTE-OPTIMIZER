def bisection(func, a, b, tolerance=1e-7, max_iterations=100):
    """Find a root by repeatedly halving an interval with a sign change."""
    a, b = float(a), float(b)
    fa, fb = func(a), func(b)
    if fa == 0:
        return {"root": a, "iterations": [], "converged": True}
    if fb == 0:
        return {"root": b, "iterations": [], "converged": True}
    if fa * fb > 0:
        raise ValueError("Bisection needs an interval [a,b] where f(a) and f(b) have opposite signs.")
    history = []
    for iteration in range(1, max_iterations + 1):
        midpoint = (a + b) / 2
        fm = func(midpoint)
        history.append({
            "iteration": iteration,
            "a": round(a, 8),
            "b": round(b, 8),
            "midpoint": round(midpoint, 8),
            "f_midpoint": round(fm, 8),
            "interval_width": round(b - a, 8)
        })
        if abs(fm) < tolerance or (b - a) / 2 < tolerance:
            return {"root": midpoint, "iterations": history, "converged": True}
        if fa * fm < 0:
            b, fb = midpoint, fm
        else:
            a, fa = midpoint, fm
    return {"root": (a + b) / 2, "iterations": history, "converged": False}
