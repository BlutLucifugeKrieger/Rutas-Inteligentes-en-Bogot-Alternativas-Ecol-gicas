import googlemaps


class GoogleMapsService:

    def __init__(self, api_key):
        self.client = googlemaps.Client(key=api_key)

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
