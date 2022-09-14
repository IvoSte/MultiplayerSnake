import random
import string


def generate_room_code(length):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))
