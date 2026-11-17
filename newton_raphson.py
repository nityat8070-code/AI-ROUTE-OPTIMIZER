def newton_raphson(func, derivative, x0, tolerance=1e-7, max_iterations=100):
    """Find a root using x[n+1] = x[n] - f(x[n])/f'(x[n])."""
    x = float(x0)
    history = []
    for iteration in range(1, max_iterations + 1):
        fx = func(x)
        dfx = derivative(x)
        if abs(dfx) < 1e-12:
            raise ValueError("Newton-Raphson stopped: derivative is too close to zero.")
        next_x = x - fx / dfx
        history.append({
            "iteration": iteration,
            "x": round(x, 8),
            "f_x": round(fx, 8),
            "derivative": round(dfx, 8),
            "next_x": round(next_x, 8),
            "error": round(abs(next_x - x), 8)
        })
        if abs(next_x - x) < tolerance:
            return {"root": next_x, "iterations": history, "converged": True}
        x = next_x
    return {"root": x, "iterations": history, "converged": False}
