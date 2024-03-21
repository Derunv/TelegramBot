import re


def format_phone_number(phone_number):
    # Remove non-digit characters
    cleaned_number = re.sub(r"\D", "", phone_number)

    # Check if the number starts with the country code
    if cleaned_number.startswith("38"):
        formatted_number = cleaned_number[2:]  # Remove country code
    else:
        formatted_number = cleaned_number

    # Check if the formatted number has the desired length
    if len(formatted_number) == 10:  # Assuming the desired length is 9 digits
        return formatted_number
    else:
        return "Error: Invalid phone number length"
