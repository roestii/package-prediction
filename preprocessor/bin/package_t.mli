(* Auto-generated from "package.atd" *)
[@@@ocaml.warning "-27-32-33-35-39"]

type location = { country: string; postal: string; lat: float; lon: float }

type package = {
  db_nr: string;
  customer_nr: int;
  articles: (string * float) list;
  weight: float;
  size: float;
  location: location;
  deliverer: string;
  is_damaged: bool
}
