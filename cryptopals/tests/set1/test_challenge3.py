import operator

from cryptopals.set1 import challenge3


def test_decrypt_message():

    message = 'I KNOW THE JOKE'
    xor_char = 'B'

    xord_message = tuple(operator.xor(item, ord(xor_char)) for item in (ord(char) for char in message))

    hex_string = ''.join(hex(item)[2:].zfill(2) for item in xord_message)

    assert challenge3.decrypt_message(hex_string) == message

def test_challenge3():

    hex_string = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    expected_message = "Cooking MC's like a pound of bacon"

    assert challenge3.decrypt_message(hex_string) == expected_message
