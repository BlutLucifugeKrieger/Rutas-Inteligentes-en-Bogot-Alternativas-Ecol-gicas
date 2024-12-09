import googlemaps
import requests


class GoogleMapsService:

    def __init__(self, api_key):
        self.client = googlemaps.Client(key=api_key)
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/directions/json"
    def get_route(self, origin, destination):
        directions = self.client.directions(
            origin,
            destination,
            mode="driving",
            departure_time="now",
            traffic_model="best_guess"
        )
        if directions:
            return directions[0]['legs'][0]['steps']
        return None

    def get_bike_routes(self, origin, destination):
        directions = self.client.directions(
            origin,
            destination,
            mode="driving",
            departure_time="now",
            traffic_model="best_guess"
        )
        if directions:
            return directions[0]['legs'][0]['steps']
        return None

    def calculate_route(self, origin, destination):
        """
        Llama a la API de Google Maps para obtener la ruta entre dos puntos.
        Args:
            origin (str): Dirección de origen.
            destination (str): Dirección de destino.

        Returns:
            dict: Respuesta de la API de Google Maps.
        """
        params = {
            "origin": origin,
            "destination": destination,
            "key": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error en la API de Google Maps: {response.status_code}, {response.text}")