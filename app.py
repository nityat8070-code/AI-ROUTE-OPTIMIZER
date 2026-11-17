from flask import Flask, render_template, request, jsonify
from route_optimizer import LOCATIONS, optimize_route

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", locations=sorted(LOCATIONS.keys()))

@app.route("/api/optimize", methods=["POST"])
def optimize():
    data = request.get_json(silent=True) or {}
    source = data.get("source")
    destination = data.get("destination")
    method = data.get("method", "both")
    try:
        result = optimize_route(source, destination, method)
        return jsonify(result)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

if __name__ == "__main__":
    app.run(debug=True)
