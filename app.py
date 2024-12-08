from datetime import datetime
from flask import Flask, request, jsonify
from rl_model import RLAgent
from google_maps_service import GoogleMapsService
import numpy as np
import tensorflow as tf
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Inicializar el agente y el servicio de Google Maps
agent = RLAgent(state_size=4, action_size=4)  # Ajustar tamaños según sea necesario
google_maps = GoogleMapsService(api_key="AIzaSyAv5SR6SwQUKbcoG-hlwep5ToGH05X03xY")


@app.route("/route", methods=["POST"])
def calculate_route():
    data = request.json
    license_plate = data.get("license_plate")
    origin = data.get("origin")
    destination = data.get("destination")

    # Validar la entrada
    if not license_plate or not origin or not destination:
        return jsonify({"error": "License plate, origin, and destination are required"}), 400

    # Verificar restricciones de pico y placa
    current_day = datetime.now().strftime("%A")
    last_digit = license_plate[-1]  # Último dígito de la placa
    restricted = is_restricted(last_digit, current_day)

    if restricted:
        # Si está restringido, recomendar rutas en bicicleta
        bike_routes = google_maps.get_bike_routes(origin, destination)  # Llamar al servicio de rutas en bicicleta
        if not bike_routes:
            return jsonify({"error": "No bike routes found"}), 500

        return jsonify({
            "restricted": True,
            "message": "El vehículo tiene pico y placa. Se recomienda usar bicicleta.",
            "bike_routes": bike_routes
        })

    # Calcular rutas normales si no hay restricción
    routes = google_maps.get_route(origin, destination)

    if routes:
        comparison = []
        best_route = None
        min_time = float('inf')

        for index, route in enumerate(routes):
            try:
                # Asegúrate de que la estructura de la respuesta es la esperada
                route_legs = route.get('legs', [])
                if route_legs:
                    first_leg = route_legs[0]
                    duration = first_leg.get('duration', {}).get('value', None)
                    distance = first_leg.get('distance', {}).get('value', None)

                    if duration is not None and distance is not None:
                        fuel_consumption_per_km = 8 / 100  # Supongamos que el consumo de combustible es 8L por cada 100 km
                        fuel_consumption = (distance / 1000) * fuel_consumption_per_km

                        comparison.append({
                            "route_index": index,
                            "duration_minutes": duration / 60,
                            "distance_km": distance / 1000,
                            "fuel_consumption_liters": fuel_consumption,
                            "instructions": [step.get('html_instructions') for step in first_leg.get('steps', [])]
                        })

                        if duration < min_time:
                            min_time = duration
                            best_route = comparison[-1]

            except (KeyError, TypeError) as e:
                # Manejar errores si la estructura de la respuesta no es la esperada
                return jsonify({"error": f"Error al procesar la ruta: {str(e)}"}), 500

        return jsonify({
            "restricted": False,
            "comparison": comparison,
            "recommended_route": best_route
        })

    return jsonify({"error": "Unable to fetch routes"}), 500


def is_restricted(last_digit, current_day):
    """Verifica si un vehículo está restringido según pico y placa."""
    restrictions = {
        "Monday": [1, 2],
        "Tuesday": [3, 4],
        "Wednesday": [5, 6],
        "Thursday": [7, 8],
        "Friday": [9, 0]

    }
    restricted_digits = restrictions.get(current_day, [])
    return int(last_digit) in restricted_digits


@app.route("/load-model", methods=["GET"])
def load_model():
    try:
        # Usar directamente la clase de métrica
        agent.model = tf.keras.models.load_model(agent.model_save_path, custom_objects={'mse': tf.keras.metrics.MeanSquaredError})
        return jsonify({"message": "Modelo cargado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    state = data.get("state")

    if not state:
        return jsonify({"error": "Se requiere un estado válido"}), 400

    try:
        state = np.reshape(state, [1, agent.state_size])
        action = agent.act(state)
        return jsonify({"action": int(action)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)




