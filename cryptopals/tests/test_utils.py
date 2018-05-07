import collections
import string

import pytest
from hypothesis import given
from hypothesis import strategies as st

from cryptopals import utils


class TestGenerateRandomHexChunks:

    @given(st.integers(max_value=256).filter(lambda x: x % 2 != 0))
    def test_odd_chunk_size(self, chunk_size):
        ''' Asserts an exception will be raised if the chunk size is an odd integer '''

        with pytest.raises(ValueError) as exc:
            utils.generate_random_hex_chunks(chunk_size=chunk_size)

    @given(st.integers(max_value=256).filter(lambda x: x % 2 == 0))
    def test_simple_case(self, chunk_size):
        ''' Happy scenario. It should generate a valid hex '''

        hex_chunk = utils.generate_random_hex_chunks(chunk_size=chunk_size)

        assert len(hex_chunk) % 2 == 0
        assert all(character in string.hexdigits for character in hex_chunk)


class TestGenerateRandomHexStrings:

    @given(st.integers(min_value=1, max_value=256).filter(lambda x: x % 2 != 0))
    def test_odd_chunk_size(self, chunk_size):

        with pytest.raises(ValueError) as exc:
            utils.generate_random_hex_strings(chunk_size=chunk_size, string_size=100)

    @given(st.integers(min_value=1, max_value=256).filter(lambda x: x % 2 != 0))
    def test_odd_string_size(self, string_size):
        with pytest.raises(ValueError) as exc:
            utils.generate_random_hex_strings(chunk_size=2, string_size=string_size)

    @given(st.integers(min_value=2, max_value=256).filter(lambda x: x % 2 == 0))
    def test_simple_case(self, string_size):

        hex_string = utils.generate_random_hex_strings(chunk_size=2, string_size=string_size)

        assert len(hex_string) == string_size
        assert all(char in string.hexdigits for char in hex_string)


class TestSplitStringIntoChunks:

    def test_string_is_empty(self):
        assert utils.split_string_into_chunks('', 2) == tuple()

    @given(st.text(min_size=1, max_size=10))
    def test_string_len_less_than_chunk_size(self, input_string):

        expected_result = (input_string[0: 11], )
        assert utils.split_string_into_chunks(input_string, 11) == expected_result


def test_split_hex_string_into_int_chunks():

    hex_string = 'd34db33f'
    expected_result = (211, 77, 179, 63)

    assert utils.split_hex_string_into_int_chunks(hex_string) == expected_result


def test_score_hex_string():

    hex_string = 'd3d34d4db3b3b33f3f'
    expected_result = collections.Counter('d3 d3 4d 4d b3 b3 b3 3f 3f'.split())

    assert isinstance(utils.score_hex_string(hex_string), collections.Counter)
    assert utils.score_hex_string(hex_string) == expected_result


def test_get_most_frequent_hex():

    hex_string = 'd3d34d4db3b3b33f3f'

    assert utils.get_most_frequent_hex(hex_string) == ('b3', 3)
