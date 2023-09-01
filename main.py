from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData, CHEAP_FLIGHTS_LIST
from notification_manager import NotificationManager


data_manager = DataManager()
data_manager.get_iata_code()

flight_search = FlightSearch()
flight_search.find_flights()

flight_data = FlightData()
for flight in CHEAP_FLIGHTS_LIST:
    if flight_data.check_price(flight_ticket_price=flight["flightprice"], lowest_price=flight["travel_lowest_price"]):
        notification = NotificationManager(city_from=flight["cityfrom"],
                                           city_to=flight["cityto"],
                                           fly_from=flight["flyfrom"],
                                           fly_to=flight["flyto"],
                                           flight_price=flight["flightprice"],
                                           currency=flight["currency"],
                                           departure=flight["flightdeparture"],
                                           arrival=flight["flightarrival"])
        notification.send_flight_info()
