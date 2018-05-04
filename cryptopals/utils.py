from typing import Tuple


def split_string_into_chunks(string: str, chunk_size: int) -> Tuple[str, ...]:
    return tuple(string[n: n + chunk_size] for n in range(0, len(string), chunk_size))


def split_hex_string_into_int_chunks(hex_string: str) -> Tuple[int, ...]:
    return tuple(int(chunk, 16) for chunk in split_string_into_chunks(hex_string, 2))
