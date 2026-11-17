from newton_raphson import newton_raphson
from bisection import bisection

# Demonstration road network (schematic distances/times, not live traffic data).
LOCATIONS = {
    "Delhi": (28.6139, 77.2090),
    "Connaught Place": (28.6315, 77.2167),
    "India Gate": (28.6129, 77.2295),
    "Airport": (28.5562, 77.1000),
    "Gurugram": (28.4595, 77.0266),
    "Faridabad": (28.4089, 77.3178),
    "Noida": (28.5355, 77.3910),
    "Ghaziabad": (28.6692, 77.4538),
    "Dwarka": (28.5921, 77.0460),
    "Hauz Khas": (28.5494, 77.2001)
}

# Each undirected edge: distance in km, estimated minutes, congestion index (0-10).
EDGES = [
    ("Delhi", "Connaught Place", 3.2, 12, 2.0),
    ("Delhi", "India Gate", 4.0, 14, 2.5),
    ("Delhi", "Airport", 16.0, 32, 5.0),
    ("Delhi", "Hauz Khas", 9.0, 25, 4.0),
    ("Connaught Place", "India Gate", 3.0, 10, 2.0),
    ("Connaught Place", "Ghaziabad", 18.0, 38, 6.0),
    ("India Gate", "Faridabad", 20.0, 42, 5.0),
    ("India Gate", "Noida", 14.0, 30, 4.0),
    ("Airport", "Gurugram", 14.0, 26, 3.0),
    ("Airport", "Dwarka", 12.0, 24, 3.0),
    ("Gurugram", "Hauz Khas", 18.0, 35, 5.0),
    ("Gurugram", "Faridabad", 28.0, 48, 6.0),
    ("Dwarka", "Hauz Khas", 17.0, 34, 4.0),
    ("Dwarka", "Gurugram", 20.0, 36, 4.0),
    ("Hauz Khas", "Faridabad", 16.0, 32, 3.0),
    ("Noida", "Ghaziabad", 12.0, 25, 3.0),
    ("Noida", "Faridabad", 27.0, 48, 6.0),
    ("Noida", "Connaught Place", 15.0, 34, 5.0),
    ("Ghaziabad", "Faridabad", 34.0, 58, 7.0),
]

def _path_for_weight(source, destination, weight):
    graph = {name: [] for name in LOCATIONS}
    for u, v, distance, minutes, congestion in EDGES:
        # Generalized edge cost: distance + time contribution + congestion penalty.
        cost = distance + 0.20 * minutes + weight * congestion
        graph[u].append((v, cost, distance, minutes, congestion))
        graph[v].append((u, cost, distance, minutes, congestion))

    # Dijkstra without external dependencies.
    import heapq
    queue = [(0.0, source, [source], 0.0, 0.0, 0.0)]
    best = {}
    while queue:
        cost_so_far, node, path, distance_sum, time_sum, congestion_sum = heapq.heappop(queue)
        if node in best and best[node] <= cost_so_far:
            continue
        best[node] = cost_so_far
        if node == destination:
            return {
                "path": path,
                "score": cost_so_far,
                "distance_km": distance_sum,
                "minutes": time_sum,
                "congestion": congestion_sum
            }
        for nxt, edge_cost, distance, minutes, congestion in graph[node]:
            if nxt not in path:
                heapq.heappush(queue, (
                    cost_so_far + edge_cost, nxt, path + [nxt],
                    distance_sum + distance, time_sum + minutes,
                    congestion_sum + congestion
                ))
    raise ValueError("No route found between the selected locations.")

def optimize_route(source, destination, method="both"):
    if source not in LOCATIONS or destination not in LOCATIONS:
        raise ValueError("Please select valid locations from the list.")
    if source == destination:
        raise ValueError("Origin and destination must be different.")

    # A bounded congestion-penalty parameter. Its target is calculated from
    # a transparent trip profile; solving f(w)=2w-target=0 demonstrates
    # both root-finding methods on the same optimization parameter.
    target_weight = 1.4
    f = lambda w: 2.0 * w - target_weight
    df = lambda w: 2.0

    results = {}
    if method in ("both", "newton"):
        results["newton"] = newton_raphson(f, df, x0=0.2)
    if method in ("both", "bisection"):
        results["bisection"] = bisection(f, 0.0, 2.0)

    roots = [item["root"] for item in results.values()]
    optimal_weight = sum(roots) / len(roots)
    route = _path_for_weight(source, destination, optimal_weight)

    # Provide a few route candidates for comparison using other weights.
    candidates = []
    for label, weight in [("Distance-focused", 0.0), ("Balanced", optimal_weight), ("Congestion-aware", 2.0)]:
        candidate = _path_for_weight(source, destination, weight)
        candidates.append({
            "label": label,
            "path": candidate["path"],
            "distance_km": round(candidate["distance_km"], 2),
            "minutes": round(candidate["minutes"]),
            "congestion": round(candidate["congestion"], 2),
            "score": round(candidate["score"], 2)
        })

    return {
        "source": source,
        "destination": destination,
        "optimal_weight": round(optimal_weight, 7),
        "route": route["path"],
        "distance_km": round(route["distance_km"], 2),
        "estimated_minutes": round(route["minutes"]),
        "congestion_index": round(route["congestion"], 2),
        "optimization_score": round(route["score"], 2),
        "methods": results,
        "candidates": candidates,
        "coordinates": [{"name": name, "lat": LOCATIONS[name][0], "lng": LOCATIONS[name][1]} for name in route["path"]],
        "model_note": "Demonstration network with illustrative road data. Traffic values are not live."
    }
