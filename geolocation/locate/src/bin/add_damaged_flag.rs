use anyhow::Result;
use clap::Parser;
use serde::{Serialize, Deserialize};
use serde_json::Value;
use std::fs::{File, OpenOptions};
use std::io::{Write, BufRead, BufReader};
use std::collections::HashMap;

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(untagged)]
enum Location {
    FullLocation(FullLocation),
    NaiveLocation(NaiveLocation),
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct Package {
    db_nr: String,
    customer_nr: String,
    deliverer: String,
    size: f64,
    weight: f64,
    location: Location,
    articles: Vec<Value>,
    is_damaged: Option<bool>,
}

#[derive(Debug, Clone, Hash, Eq, PartialEq, Serialize, Deserialize)]
struct NaiveLocation {
    country: String,
    postal: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct FullLocation {
    country: String,
    postal: String,
    lat: f64,
    lon: f64
}

#[derive(Parser, Debug)]
struct Args {
    #[arg(short, long)]
    source_file: String,

    #[arg(short, long)]
    target_file: String,

    #[arg(short, long)]
    output_file: String,
}

fn main() -> Result<()> {
    let Args { source_file, target_file, output_file } = Args::parse();
    let source_file = File::open(source_file)?;
    let target_file = File::open(target_file)?;

    let mut output_file = OpenOptions::new()
        .append(true)
        .create(true)
        .open(output_file)?;

    let source_buf = BufReader::new(source_file);
    let mut source_lines = source_buf.lines();
    
    let mut source_map = HashMap::new();

    while let Some(Ok(line)) = source_lines.next() {
        let package = serde_json::from_str::<Package>(&line)?;
        source_map.insert(package.db_nr, package.is_damaged.unwrap());
    }

    let target_buf = BufReader::new(target_file);
    let mut target_lines = target_buf.lines();

    let mut target_packages = Vec::with_capacity(source_map.len());

    while let Some(Ok(line)) = target_lines.next() {
        let mut package = serde_json::from_str::<Package>(&line)?;
        println!("{:?}", package.location);
        let is_damaged = source_map.get(&package.db_nr)
            .expect("db_nr to exist");

        package.is_damaged = Some(*is_damaged);
        target_packages.push(package);
    }

    for package in &target_packages {
        let content = serde_json::to_string(package)?;
        writeln!(output_file, "{}", content)?;
    }

    Ok(())
}
