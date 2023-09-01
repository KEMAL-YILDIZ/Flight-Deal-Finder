import smtplib
MY_GMAIL = "GMAIL"
MY_PASSWORD = "PASSWORD"


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self, city_from, city_to, fly_from, fly_to, flight_price, currency, departure, arrival):
        self.city_from = city_from
        self.city_to = city_to
        self.fly_from = fly_from
        self.fly_to = fly_to
        self.price = flight_price
        self.currency = currency
        self.departure = departure
        self.arrival = arrival

    def send_flight_info(self):
        message = f"Low price alert! \nonly {self.price} {self.currency} to fly from {self.city_from}-{self.fly_from}" \
                  f" to {self.city_to}-{self.fly_to}, from {self.departure} to {self.arrival}"
        with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_GMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_GMAIL, to_addrs=MY_GMAIL, msg=message)
