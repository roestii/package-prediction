use anyhow::Result;
use async_recursion::async_recursion;
use rand::{Rng, thread_rng};
use std::collections::{HashMap, HashSet};
use clap::Parser;
use reqwest::ClientBuilder;
use serde_json::Value;
use std::{fs::{File, OpenOptions}, io::{Write, BufRead, BufReader}};
use serde::{Serialize, Deserialize};

#[derive(Parser)]
struct Args {
    #[arg(short, long)]
    input_file: String,

    #[arg(short, long)]
    output_file: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(untagged)]
enum Location {
    NaiveLocation(NaiveLocation),
    FullLocation(FullLocation),
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
    is_damaged: bool,
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

#[tokio::main]
async fn main() -> Result<()> {
    let Args { input_file, output_file } = Args::parse();
    let input_file = File::open(input_file)?;
    let mut output_file = OpenOptions::new()
        .append(true)
        .create(true)
        .open(output_file)?;

    let buf_reader = BufReader::new(input_file);
    let mut lines = buf_reader.lines();
    
    let mut locations: HashSet<NaiveLocation> = HashSet::new();
    let mut packages: Vec<Package> = Vec::with_capacity(100000);

    while let Some(Ok(line)) = lines.next() {
        let package: Package = serde_json::from_str(&line)?;     
        let location = match package.location {
            Location::NaiveLocation(ref l) => l,
            _ => unreachable!()
        };

        locations.insert(location.clone());
        packages.push(package);
    }

    let len = locations.len();
    println!("{}", len);

    let mut location_map: HashMap<NaiveLocation, FullLocation> = HashMap::with_capacity(locations.len());

    let user_agents = vec![
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/98.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4654.45 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
    ];


    let mut rng = thread_rng();
     
    for (idx, location) in locations.into_iter().enumerate() {
        //tokio::time::sleep(tokio::time::Duration::from_secs(1)).await;
        let u = rng.gen_range(0..user_agents.len());
        let user_agent = user_agents[u];

        let client = ClientBuilder::new()
            .user_agent(user_agent)
            .build()
            .expect("working client");

        if idx % 20 == 0 {
            println!("{}", (idx * 100) / len);
        }

        let Some((lat, lon)) = geolocate(client, &location.country, &location.postal).await else {
            continue;
        };
        
        let full_location = FullLocation {
            country: location.country.clone(),
            postal: location.postal.clone(),
            lat,
            lon,
        };

        location_map.insert(location, full_location);
    }

    let packages: Vec<Package> = packages.into_iter()
        .filter_map(|package| {
            let location = match package.location {
                Location::NaiveLocation(ref l) => l.clone(),
                _ => unreachable!()
            };

            location_map.get(&location).map(|full_location| {
                let mut package = package.clone();
                package.location = Location::FullLocation(full_location.clone());
                package
            })
        })
        .collect();

    for package in &packages {
        let content = serde_json::to_string(package)?;
        writeln!(output_file, "{}", content)?;
    }
    
    Ok(())
}

#[async_recursion]
async fn geolocate(client: reqwest::Client, country: &str, postal: &str) -> Option<(f64, f64)> {
    let url = "https://nominatim.openstreetmap.org/search?";
    let url = format!("{}country={}&postalcode={}&format=json", url, country, postal);
    let response = client.get(&url)
        .send()
        .await
        .expect("valid url")
        .json::<Value>()
        .await
        .expect("valid json");

    match response {
        Value::Array(inner) => {
            if inner.len() == 0 {
                return None;
            }

            let lat: f64 = inner[0].get("lat")
                .expect("lat to exist")
                .as_str()
                .expect("lat to be a string")
                .parse()
                .expect("lat to be a float");

            let lon: f64 = inner[0].get("lon")
                .expect("lon to exist")
                .as_str()
                .expect("lon to be a string")
                .parse()
                .expect("lon to be a float");

            println!("gotcha");
            Some((lat, lon))
        },
        _ => {
            println!("retrying");
            geolocate(client, country, postal).await
        }
    }
}
