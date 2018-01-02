#[macro_use] extern crate maplit;
use std::collections::HashMap;

extern crate num_traits;
use num_traits::pow;


pub type Decimal = u32;
pub type Hex = String;
pub type Binary = String;
pub type B64 = String;


fn get_hex_to_bin_map() -> HashMap<char, Binary> {

    let hex_numbers = hashmap!{
        '0' => Binary::from("0000"),
        '1' => Binary::from("0001"),
        '2' => Binary::from("0010"),
        '3' => Binary::from("0011"),
        '4' => Binary::from("0100"),
        '5' => Binary::from("0101"),
        '6' => Binary::from("0110"),
        '7' => Binary::from("0111"),
        '8' => Binary::from("1000"),
        '9' => Binary::from("1001"),
        'A' => Binary::from("1010"),
        'B' => Binary::from("1011"),
        'C' => Binary::from("1100"),
        'D' => Binary::from("1101"),
        'E' => Binary::from("1110"),
        'F' => Binary::from("1111"),
    };

    return hex_numbers;
}


fn get_bin_to_hex_map() -> HashMap<Binary, Hex> {

    let hex_numbers = hashmap!{
        Binary::from("0000") => Hex::from("0"),
        Binary::from("0001") => Hex::from("1"),
        Binary::from("0010") => Hex::from("2"),
        Binary::from("0011") => Hex::from("3"),
        Binary::from("0100") => Hex::from("4"),
        Binary::from("0101") => Hex::from("5"),
        Binary::from("0110") => Hex::from("6"),
        Binary::from("0111") => Hex::from("7"),
        Binary::from("1000") => Hex::from("8"),
        Binary::from("1001") => Hex::from("9"),
        Binary::from("1010") => Hex::from("A"),
        Binary::from("1011") => Hex::from("B"),
        Binary::from("1100") => Hex::from("C"),
        Binary::from("1101") => Hex::from("D"),
        Binary::from("1110") => Hex::from("E"),
        Binary::from("1111") => Hex::from("F"),
    };

    return hex_numbers;
}


pub trait ToDecimal {
    fn to_decimal(&self) -> Decimal;
}


pub trait ToHex {
    fn to_hex(&self) -> Hex;
}


pub trait ToBinary {
    fn to_binary(&self) -> Binary;
}


pub trait ToB64 {
    fn to_b64(&self) -> B64;
}


impl ToBinary for Hex {
    fn to_binary(&self) -> Binary {
        let hex_numbers = get_hex_to_bin_map();
        let mut _binary = Binary::with_capacity(self.len());
        for c in self.chars() {
            _binary.push_str(hex_numbers.get(&c.to_uppercase().next().unwrap()).unwrap());
        }
        _binary
    }
}


impl ToHex for Binary {
    fn to_hex(&self) -> Hex {
        let bin_numbers = get_bin_to_hex_map();
        let subs = self
            .chars()
            .collect::<Vec<_>>()
            .chunks(4)
            .map(|c| c.iter().cloned().collect::<Binary>())
            .map(|b| bin_numbers.get(&b).unwrap())
            .map(|h| h.to_string()).collect();
        subs
    }
}


impl ToDecimal for Binary {
    fn to_decimal(&self) -> Decimal {
        let _decimal: Decimal = self.chars()
            .zip((0..self.len()).rev())
            .map(|(n, e)| n.to_digit(2).unwrap() * pow(2, e))
            .sum();
        _decimal
    }
}


// impl ToB64 for Hex {
//     fn to_b64(&self) -> B64 {
//         self.to_binary()
//     }
// }
