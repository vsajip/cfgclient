use cfg_lib::config::*;
use std::io::Cursor;

fn main() {
    let source = "key: 'Hello, world!'";

    let mut cfg = Config::new();
    cfg.load(Box::new(Cursor::new(source))).expect("couldn't load from source");

    println!("{}", cfg.get("key").unwrap());
}
