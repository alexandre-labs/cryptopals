extern crate numberconv;
use numberconv::{ToBinary, ToDecimal};

fn main() {

    let foo = String::from("de4db33f");
    println!("{:?}", foo.to_binary().to_decimal());
}
