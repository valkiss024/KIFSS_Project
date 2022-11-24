import random
import string


def generate_password(length):
    """Method to generate a random password for a given length"""
    password = "".join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return password
