'''
Break repeating-key XOR


It is officially on, now.

This challenge isn't conceptually hard, but it involves actual error-prone coding.
The other challenges in this set are there to bring you up to speed. This one is there to qualify you.
If you can do this one, you're probably just fine up to Set 6.

There's a file here. It's been base64'd after being encrypted with repeating-key XOR.

Decrypt it.

Here's how:

* Let KEYSIZE be the guessed length of the key; try values from 2 to (say) 40.

* Write a function to compute the edit distance/Hamming distance between two strings.
The Hamming distance is just the number of differing bits. The distance between:

this is a test
and
wokka wokka!!!

is 37. Make sure your code agrees before you proceed.


* For each KEYSIZE, take the first KEYSIZE worth of bytes, and the second KEYSIZE worth of bytes,
and find the edit distance between them. Normalize this result by dividing by KEYSIZE.

* The KEYSIZE with the smallest normalized edit distance is probably the key.
You could proceed perhaps with the smallest 2-3 KEYSIZE values. Or take 4 KEYSIZE blocks instead of 2 and average the distances.

* Now that you probably know the KEYSIZE: break the ciphertext into blocks of KEYSIZE length.

* Now transpose the blocks: make a block that is the first byte of every block,
and a block that is the second byte of every block, and so on.

* Solve each block as if it was single-character XOR. You already have code to do this.

* For each block, the single-byte XOR key that produces the best looking histogram is the repeating-key XOR key byte for
that block. Put them together and you have the key.


This code is going to turn out to be surprisingly useful later on.
Breaking repeating-key XOR ("Vigenere") statistically is obviously an academic exercise, a "Crypto 101" thing.
But more people "know how" to break it than can actually break it, and a similar technique breaks something much more important.

No, that's not a mistake.
We get more tech support questions for this challenge than any of the other ones. We promise, there aren't any blatant errors
in this text. In particular: the "wokka wokka!!!" edit distance really is 37.
'''


import base64
import collections
import functools
import itertools
import operator
import string
from typing import ByteString, Generator, Iterator, Tuple, Union

from cryptopals import utils


def get_key_size_and_hamming_distance(keysize_range: Tuple[int], encrypted_text: str) -> Iterator:
    '''* For each KEYSIZE, take the first KEYSIZE worth of bytes, and the second KEYSIZE worth of bytes,
    and find the edit distance between them. Normalize this result by dividing by KEYSIZE.
    '''

    def _calculate_distance(data: Iterator, keysize: int) -> Tuple[int, float]:
        return keysize, (utils.calculate_hamming_distance(
            ''.join(itertools.islice(data, keysize)),
            ''.join(itertools.islice(data, keysize))
        ) / keysize)

    return map(lambda data_keysize: _calculate_distance(data_keysize[0], data_keysize[1]),
               zip(itertools.cycle((iter(encrypted_text), )), range(*keysize_range)))


def break_in_blocks_and_transpose(encrypted_text: str, blocksize: int) -> Tuple[str]:

    def _transpose(data):

        if data == ('',) * len(data):
            return tuple()

        return (
            (''.join(map(lambda x: x[0] if len(x) > 0 else x, data)), ) +
            _transpose(tuple(map(operator.itemgetter(slice(1, None, None)), data)))
        )

    return _transpose(utils.split_string_into_chunks(encrypted_text, blocksize))


def get_best_ascii_rate_on_single_key_xors(encrypted_text: str) -> Tuple[int, float]:

    # Instead of using most frequent char, I'll use all the hex combinations...like I did on the challenge 4
    # most_frequent, _ = list(
    #     filter(lambda item: item[0] in string.ascii_letters, collections.Counter(encrypted_text).most_common())
    # )[0]

    def get_hex_combinations_as_int() -> Iterator:
        return map(lambda comb: int('{}{}'.format(*comb), 16), utils.get_hex_combinations())

    def do_single_key_xor(encrypted_text: str, key: int) -> Tuple[int, str]:
        return key, ''.join(chr(operator.xor(key, ord(char))) for char in encrypted_text)

    def do_single_key_xor_for_all_combs(encrypted_text: str) -> Iterator:
        return map(functools.partial(do_single_key_xor, encrypted_text), get_hex_combinations_as_int())

    def get_ascii_char_rate(key: int, decrypted_text: str) -> Tuple[int, float]:
        return key, sum(1 if (char in string.ascii_letters or char == ' ') else 0 for char in decrypted_text) / len(decrypted_text)

    return max(
        map(lambda key_text: get_ascii_char_rate(key_text[0], key_text[1]), do_single_key_xor_for_all_combs(encrypted_text)),
        key=lambda key_rate: key_rate[1]
    )


def get_possible_repeating_key_xor_key(encrypted_text: str, keysize: int) -> str:
    return ''.join(chr(key) for key, score in
                   map(get_best_ascii_rate_on_single_key_xors, break_in_blocks_and_transpose(encrypted_text, keysize)))


def decrypt_repeating_key_xor(base64d_file_data: str, keysize_range: Tuple[int]):

    def get_3_smallest_keysize_values(encrypted_text: str, keysize_range: Tuple[int]):
        return map(
            lambda keysize_distance: (encrypted_text, keysize_distance[0]),
            sorted(get_key_size_and_hamming_distance(keysize_range, encrypted_text), key=lambda ks_dist: ks_dist[1])[0:3]
        )

    def get_possible_key_and_encrypted_text(base64d_file_data: str):
        return map(
            lambda text_keysize: (get_possible_repeating_key_xor_key(text_keysize[0], text_keysize[1]), text_keysize[0]),
            get_3_smallest_keysize_values(base64.b64decode(base64d_file_data.encode()).decode(), keysize_range)
        )

    def decrypt_text(key: str, text: str) -> str:
        return ''.join(map(chr, utils.do_repeating_key_xor(text, key)))

    return map(
        lambda key_text: decrypt_text(key_text[0], key_text[1]),
        get_possible_key_and_encrypted_text(base64d_file_data)
    )
