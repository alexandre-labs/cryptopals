"""

Single-byte XOR cipher

The hex encoded string:

1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736

... has been XOR'd against a single character. Find the key, decrypt the message.

You can do this by hand. But don't: write code to do it for you.

How? Devise some method for "scoring" a piece of English plaintext. Character frequency is a good metric.
Evaluate each output and choose the one with the best score.
Achievement Unlocked

You now have our permission to make "ETAOIN SHRDLU" jokes on Twitter.
"""
from operator import xor
from typing import Optional

from cryptopals import utils


def decrypt_message(hex_string: str, most_frequent_hex: Optional[str] = None) -> str:

    if not most_frequent_hex:

        # The underscore would be the score. 'score' means how many times this hex appears in the string...
        most_frequent_hex, _ = utils.get_most_frequent_hex(hex_string)

    # mf_ -> most frequent
    # Getting the ascii letter related to the most frequent hex, but in uppercase
    mf_ascii_int = ord(chr(int(most_frequent_hex, 16)).upper())

    int_chunks = utils.split_hex_string_into_int_chunks(hex_string)

    return ''.join(chr(xor(mf_ascii_int, chunk)) for chunk in int_chunks)
