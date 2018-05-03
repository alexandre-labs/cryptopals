from typing import Tuple


def split_string_into_chunks(string: str, chunk_size: int) -> Tuple[str, ...]:
    return tuple(string[n: n + chunk_size] for n in range(0, len(string), chunk_size))
