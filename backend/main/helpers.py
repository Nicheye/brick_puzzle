import random
import string
from datetime import datetime


def generate_random_code(length=6):
    characters = string.ascii_letters + string.digits  # Includes both letters and digits
    code = ''.join(random.choices(characters, k=length))
    return code


def parse_date_string(date_string: str):
    # Assuming the date_string is in the format "MM/DD" and you want to use the current year
    current_year = datetime.now().year
    date_format = "%m/%d"

    try:
        # Combine the current year with the provided month and day
        full_date_string = f"{current_year}/{date_string}"
        # Parse the date string to a datetime object
        date_object = datetime.strptime(full_date_string, f"%Y/{date_format}").date()
        return date_object
    except ValueError:
        # Handle the error if the date_string is invalid
        raise ValueError("Date string is not in the correct format. Use MM/DD.")


def parse_ff_ls(card: str):
    first_four = int(card[:4])
    last_six = int(card[-6:])
    return first_four, last_six