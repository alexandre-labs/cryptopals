"""
Fixed XOR

Write a function that takes two equal-length buffers and produces their XOR combination.

If your function works properly, then when you feed it the string:

1c0111001f010100061a024b53535009181c

... after hex decoding, and when XOR'd against:

686974207468652062756c6c277320657965

... should produce:

746865206b696420646f6e277420706c6179
"""
import operator

from cryptopals.utils import split_hex_string_into_int_chunks


def get_fixed_xor(hex_string_a: str, hex_string_b: str) -> str:

    # Decode hex strings to int and zip them
    zipped_int_chunks = zip(split_hex_string_into_int_chunks(hex_string_a), split_hex_string_into_int_chunks(hex_string_b))

    # xor each pair and encode as hex again (ignore the first two items '0x')
    return ''.join(hex(operator.xor(pair[0], pair[1]))[2:] for pair in zipped_int_chunks)
