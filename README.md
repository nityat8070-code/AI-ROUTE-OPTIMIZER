# RouteIQ — AI-Based Route Optimization (Academic Demonstration)

A Flask web application demonstrating route selection on a small, illustrative road network and the implementation of Newton-Raphson and Bisection root-finding methods.

## Features
- Flask backend and responsive HTML/CSS/JavaScript frontend.
- Dijkstra shortest-path search on an illustrative road graph.
- Newton-Raphson implementation in `newton_raphson.py`.
- Bisection implementation in `bisection.py`.
- Iteration tables for both methods and route-profile comparison.
- Leaflet map using OpenStreetMap tiles.

## Important academic note
The road network, distances, travel times and congestion values are illustrative demo data, not live traffic. The numerical methods solve the explicit parameter equation `f(w) = 2w - 1.4 = 0`. The resulting congestion-penalty weight is used in the generalized route edge cost:

`edge_cost = distance_km + 0.20 * estimated_minutes + w * congestion_index`

Dijkstra's algorithm selects a path under that cost. Newton-Raphson and Bisection are numerical root-finding methods; they are not themselves AI models. This project is an explainable numerical optimization demonstration rather than a trained machine-learning system.

## Run on Windows (VS Code terminal)
1. Extract the ZIP.
2. Open the extracted `AI_Route_Optimizer` folder in VS Code.
3. Create a virtual environment:
   `py -m venv venv`
4. Activate it:
   `venv\Scripts\activate`
5. Install dependencies:
   `pip install -r requirements.txt`
6. Start the website:
   `python app.py`
7. Open the local address shown in the terminal (normally `http://127.0.0.1:5000`).

Internet is needed for OpenStreetMap tiles and Leaflet CDN assets. The backend route calculations run locally.
