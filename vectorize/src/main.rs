use std::{fs::{File, OpenOptions}, io::{BufReader, BufRead}};
use std::io::Write;

use anyhow::Result;
use haversine::{Location, distance};
use serde::{Serialize, Deserialize};
use clap::Parser;

#[derive(Parser)]
struct Args {
    #[clap(short, long)]
    input_file: String,

    #[clap(short, long)]
    output_file: String,
}

#[derive(Debug, Serialize, Deserialize)]
struct Package {
    db_nr: String, 
    vec_repr: Vec<f64>,
    is_damaged: u8,
}

fn main() -> Result<()> {
    let Args { input_file, output_file } = Args::parse();

    let file = File::open(input_file)?;
    let buf = BufReader::new(file);
    let mut lines = buf.lines();

    let mut output_file = OpenOptions::new()
        .create(true)
        .append(true)
        .open(output_file)?;

    while let Some(Ok(line)) = lines.next() {
        let mut package: Package = serde_json::from_str(&line)?;

        let longitude = package.vec_repr[2];
        let latitude = package.vec_repr[3];
        //let longitude = package.vec_repr.remove(2);
        //let latitude = package.vec_repr.remove(2);

        let espelkamp = (52.382428757928416, 8.62005272623726);
        let dest = (latitude, longitude);

        let dest_loc = Location {
            latitude: dest.0,
            longitude: dest.1,
        };

        //Latitude and longitude of Espelkamp (the place where the packages are sent from)

        let espelkamp_loc = Location {
            latitude: espelkamp.0,
            longitude: espelkamp.1,
        };

        let dist = distance(espelkamp_loc, dest_loc, haversine::Units::Kilometers);
        package.vec_repr.insert(2, dist);

        let stringified = serde_json::to_string(&package)?;
        writeln!(output_file, "{}", stringified)?;
    }

    Ok(())
}
