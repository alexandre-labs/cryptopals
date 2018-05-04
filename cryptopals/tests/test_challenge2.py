from cryptopals.set1 import challenge2


def test_get_fixed_xor():

    hex_string_a = '1c0111001f010100061a024b53535009181c'
    hex_string_b = '686974207468652062756c6c277320657965'
    expected_result = '746865206b696420646f6e277420706c6179'

    assert challenge2.get_fixed_xor(hex_string_a, hex_string_b) == expected_result
