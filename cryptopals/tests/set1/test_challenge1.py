from hypothesis import given
from hypothesis import strategies as st

from cryptopals.set1 import challenge1
from cryptopals.utils import generate_random_hex_strings


def test_convert_hex_to_ascii():

    hex_string = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
    expected_string = "I'm killing your brain like a poisonous mushroom"

    assert challenge1.convert_hex_to_ascii(hex_string) == expected_string


@given(st.builds(generate_random_hex_strings, st.integers(2, 2), st.integers(256, 256)))
def test_convert_hex_to_ascii_hypothesis(hex_string: str):

    expected_string = ''.join(chr(n) for n in bytes.fromhex(hex_string))

    assert challenge1.convert_hex_to_ascii(hex_string) == expected_string


def test_convert_ascii_to_base64():

    ascii_string = "I'm killing your brain like a poisonous mushroom"
    expected_string = 'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'

    assert challenge1.convert_ascii_to_base64(ascii_string).decode('ascii') == expected_string
