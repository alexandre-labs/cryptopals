from cryptopals.set1 import challenge4


def test_find_xord_hex_string():

    expected_result = 'Now that the party is jumping'

    assert challenge4.find_xord_hex_string()[1].strip() == expected_result
