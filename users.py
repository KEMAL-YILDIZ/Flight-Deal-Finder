import requests
import data_manager


class Users:
    def __init__(self):
        self.first_name = input("What's your first name?\n")
        self.last_name = input("What's your last name?\n")
        email = input("What's your email?\n")
        email_again = input("What's your email again?\n")
        if email != email_again:
            email_again = input("Please enter your correct email,"
                                " there will be no other chance to enter your second email")
        if email == email_again:
            self.actual_email = email
            print("You're in the club!")
        else:
            print("You've your email isn't identical, please restart the program")

    def save_user_info(self):
        sheety_headers = {"Authorization": data_manager.SHEETY_TOKEN}
        sheety_params = {
            "user": {
                "firstName": self.first_name,
                "lastName": self.last_name,
                "email": self.actual_email}
        }

        sheety_response = requests.post(url=data_manager.SHEETY_USERS_ENDPOINT,
                                        json=sheety_params,
                                        headers=sheety_headers)
        sheety_response.raise_for_status()
