import random
import string

def generate_url_string(max_length=5):
    length = random.randint(5, max_length)
    random_string = ''.join(random.choice(string.ascii_letters) for _ in range(length))
    return random_string
