import time
import uuid

BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def custom_hash(string: str) -> int:
    """
    A custom hash function to convert a string into a numeric representation.

    Args:
        string (str): The string to be hashed.

    Returns:
        int: The numeric representation of the hashed string.
    """
    # initializing the hash value
    hash_value = 0

    # Looping over each character in the string
    for char in string:
        # ord(char) returns the ASCII value of the character.
        # The hash value is updated with the included prime number (31), and ord(char).
        # The modulo operator (%) ensures the hash remains a 32-bit unsigned integer.
        hash_value = (31 * hash_value + ord(char)) % 2 ** 32

    # Return the final hash value as an integer.
    return hash_value


def generate_encoded_string() -> str:
    """
    Generate a short URL with base58 encoding.

    The function uses a combination of the current timestamp and a hash of a
    unique id to create a unique string. This string is converted into a base58
    string to achieve a shorter URL.

    Returns:
        str: The short encoded URL.
    """

    # Generate a unique identifier (UUID)
    unique_id = uuid.uuid4()

    # Convert UUID to string and hash it to obtain a numeric representation
    unique_id_numeric = custom_hash(str(unique_id))

    # Get current timestamp (in milliseconds)
    timestamp_ms = int(time.time() * 1000)

    # Combine timestamp and unique identifier to form a unique string
    unique_string = str(timestamp_ms) + str(unique_id_numeric)

    # Convert unique string to base10 integer
    base10_num = int(unique_string)

    # Encode base10 integer to base58 string
    short_url = base58_encode(base10_num)

    return short_url


def base58_encode(num: int) -> str:
    """
    Encode a base10 integer into base58.

    Args:
        num (int): The number in base10 format.

    Returns:
        str: The number in base58 format.
    """
    encoded = ''
    # Use a while loop to repeatedly divide the number by 58
    while num > 0:
        # Use the divmod function that divides the number and returns the quotient and remainder
        num, remainder = divmod(num, 58)
        # Add the base58 character corresponding to the remainder at the beginning of the encoded string
        encoded = BASE58_ALPHABET[remainder] + encoded
    # Return the base58 encoded string
    return encoded
