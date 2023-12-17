(* Auto-generated from "package.atd" *)
[@@@ocaml.warning "-27-32-33-35-39"]

type location = Package_t.location = {
  country: string;
  postal: string;
  lat: float;
  lon: float
}

type package = Package_t.package = {
  db_nr: string;
  customer_nr: int;
  articles: (string * float) list;
  weight: float;
  size: float;
  location: location;
  deliverer: string;
  is_damaged: bool
}

val write_location :
  Buffer.t -> location -> unit
  (** Output a JSON value of type {!type:location}. *)

val string_of_location :
  ?len:int -> location -> string
  (** Serialize a value of type {!type:location}
      into a JSON string.
      @param len specifies the initial length
                 of the buffer used internally.
                 Default: 1024. *)

val read_location :
  Yojson.Safe.lexer_state -> Lexing.lexbuf -> location
  (** Input JSON data of type {!type:location}. *)

val location_of_string :
  string -> location
  (** Deserialize JSON data of type {!type:location}. *)

val write_package :
  Buffer.t -> package -> unit
  (** Output a JSON value of type {!type:package}. *)

val string_of_package :
  ?len:int -> package -> string
  (** Serialize a value of type {!type:package}
      into a JSON string.
      @param len specifies the initial length
                 of the buffer used internally.
                 Default: 1024. *)

val read_package :
  Yojson.Safe.lexer_state -> Lexing.lexbuf -> package
  (** Input JSON data of type {!type:package}. *)

val package_of_string :
  string -> package
  (** Deserialize JSON data of type {!type:package}. *)

