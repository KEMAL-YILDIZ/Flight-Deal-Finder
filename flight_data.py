CHEAP_FLIGHTS_LIST = []


class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self):
        self.flights_list = CHEAP_FLIGHTS_LIST

    @staticmethod
    def check_price(flight_ticket_price: str, lowest_price: str) -> bool:
        if int(flight_ticket_price) < int(lowest_price):
            return True
