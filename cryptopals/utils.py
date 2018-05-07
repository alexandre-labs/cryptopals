import collections
import random
import string
from typing import Tuple


def generate_random_hex_chunks(chunk_size: int = 2) -> str:

    if not(chunk_size % 2 == 0):
        raise ValueError('Chunk size should be a multiple of 2.')

    return ''.join(random.choices(string.hexdigits, k=chunk_size))


def generate_random_hex_strings(chunk_size:int = 2, string_size:int  = 256) -> str:

    if not all([chunk_size % 2 == 0, string_size % 2 == 0]):
        raise ValueError('Chunk size and string_size should be a multiple of 2.')

    return ''.join(generate_random_hex_chunks(chunk_size) for n in range(0,  int(string_size / chunk_size)))


def split_string_into_chunks(string: str, chunk_size: int) -> Tuple[str, ...]:
    return tuple(string[n: n + chunk_size] for n in range(0, len(string), chunk_size))


def split_hex_string_into_int_chunks(hex_string: str) -> Tuple[int, ...]:
    return tuple(int(chunk, 16) for chunk in split_string_into_chunks(hex_string, 2))


def score_hex_string(hex_string: str) -> collections.Counter:
    return collections.Counter(split_string_into_chunks(hex_string, 2))


def get_most_frequent_hex(hex_string: str) -> Tuple[str, int]:
    return max(score_hex_string(hex_string).items(), key=lambda pair: pair[1])
