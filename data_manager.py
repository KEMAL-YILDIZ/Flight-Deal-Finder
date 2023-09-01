import requests


SHEETY_PRICES_ENDPOINT = "END_POINT"
SHEETY_TOKEN = "API_TOKEN"
TEQUILA_ENDPOINT = "END_POINT"
TEQUILA_API_KEY = "API_KEY"
cities_data = []


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        # google sheet must have 3 fileds: 1.City 2.IATA Code 3.Lowest Price
        self.SHEETY_ENDPOINT = SHEETY_PRICES_ENDPOINT
        self.SHEETY_TOKEN = SHEETY_TOKEN
        self.TEQUILA_API_KEY = TEQUILA_API_KEY
        self.TEQUILA_ENDPOINT = TEQUILA_ENDPOINT

    def get_iata_code(self):
        global cities_data
        sheety_headers = {"Authorization": self.SHEETY_TOKEN}
        sheety_response = requests.get(url=self.SHEETY_ENDPOINT, headers=sheety_headers)

        # list that has all city data one by one,
        # so we can iterate through their ["city"] and use tequila_response to get their IATA code
        cities_data = sheety_response.json()["prices"]

        tequila_location_endpoint = f"{self.TEQUILA_ENDPOINT}/locations/query"
        tequila_headers = {"apikey": self.TEQUILA_API_KEY}

        # the for loop is for getting the iata code for each country and after that we add it to the
        # correct row in the gsheet
        if cities_data[0]["iataCode"] == "":
            # this index variable is for iterating through the rows of the gsheet and both the city names and
            # the index is set to 2 is bc the gsheet first row is 2
            index = 2
            for city_data in cities_data:
                tequila_parameters = {
                    "term": city_data["city"],
                    "location_types": "city"
                }

                tequila_response = requests.get(url=tequila_location_endpoint,
                                                headers=tequila_headers,
                                                params=tequila_parameters)
                tequila_response.raise_for_status()
                # this is the IATA code where Paris will be PAR
                iata_code = tequila_response.json()["locations"][0]["code"]

                # and here we're starting to edit the gsheet to add iata_code to it
                new_parameter = {
                    "price": {
                        "iataCode": iata_code
                    }
                }
                edit_response = requests.put(url=f"{self.SHEETY_ENDPOINT}/{index}",
                                             json=new_parameter,
                                             headers=sheety_headers)
                edit_response.raise_for_status()
                index += 1
