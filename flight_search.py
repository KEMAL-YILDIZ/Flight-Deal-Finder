import requests
import datetime as dt
from flight_data import CHEAP_FLIGHTS_LIST
import data_manager


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.SHEETY_ENDPOINT = data_manager.SHEETY_PRICES_ENDPOINT
        self.SHEETY_TOKEN = data_manager.SHEETY_TOKEN
        self.TEQUILA_API_KEY = data_manager.TEQUILA_API_KEY
        self.TEQUILA_ENDPOINT = data_manager.TEQUILA_ENDPOINT

    def find_flights(self):
        # sheety_headers = {"Authorization": self.SHEETY_TOKEN}
        # sheety_response = requests.get(url=self.SHEETY_ENDPOINT, headers=sheety_headers)
        # cities_data = [item for item in sheety_response.json()["prices"]]
        # cities_data = ["PAR", "BER", "TYO", "SYD", "IST", "KUL", "NYC", "SFO", "CPT"]
        cities_data = data_manager.cities_data
        tequila_headers = {"apikey": self.TEQUILA_API_KEY}
        today = dt.datetime.now()
        aimed_month = today.month
        aimed_year = today.year
        aimed_day = today.day
        if today.month + 6 > 12:
            aimed_year += 1
            aimed_month -= 6
        if aimed_day >= 25:
            aimed_day -= 5
        after_6months = dt.datetime(year=aimed_year, month=aimed_month, day=aimed_day)
        for city_data in cities_data:
            tequila_parameters = {
                "fly_from": "ANK",
                "fly_to": city_data["iataCode"],
                "date_from": today.strftime("%d/%m/%Y"),
                "date_to": after_6months.strftime("%d/%m/%Y")
            }

            # getting the flight info from ankara to the wanted city
            tequila_response = requests.get(url=f"{self.TEQUILA_ENDPOINT}/v2/search",
                                            params=tequila_parameters,
                                            headers=tequila_headers)
            tequila_response.raise_for_status()
            try:
                flight_info = tequila_response.json()["data"][0]
            except IndexError:
                print("flight to destination not found")
                continue
            else:
                cheap_flight_data = {"cityfrom": flight_info["cityFrom"],
                                     "cityto": flight_info["cityTo"],
                                     "flightprice": flight_info["price"],
                                     "flyfrom": flight_info["flyFrom"],
                                     "flyto": flight_info["flyTo"],
                                     "cityfromcode": flight_info["cityCodeFrom"],
                                     "citytocode": flight_info["cityCodeTo"],
                                     "currency": tequila_response.json()["currency"],
                                     "flightdeparture":
                                         (flight_info["route"][0]["local_departure"]).split("T")[0],
                                     "flightarrival":
                                         (flight_info["route"][0]["local_arrival"]).split("T")[0],
                                     "travel_lowest_price": city_data["lowestPrice"]}
                CHEAP_FLIGHTS_LIST.append(cheap_flight_data)
