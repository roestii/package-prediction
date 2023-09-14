open Core 

type t = 
    | Abholer
    | Abholung
    | Auslfa
    | Dhl
    | Infehler
    | Kep
    | Meyerjumb
    | Post
    | Sped
    | Speddsv
    | Sped_osna
    | Tour_sped
    | Ups
    | Ups_a_geb
    | Ups_ch
    | Werkvk
[@@deriving show]

let of_string str = 
    match str with 
    | "ABHOLER"-> Abholer
    | "ABHOLUNG"-> Abholung
    | "AUSL._FA"-> Auslfa
    | "DHL"-> Dhl
    | "IN. FEHLER"-> Infehler
    | "KEP"-> Kep
    | "MEYER JUMB"-> Meyerjumb
    | "POST"-> Post
    | "SPED"-> Sped
    | "SPED/DSV"-> Speddsv
    | "SPED_OSNA"-> Sped_osna
    | "TOUR_SPED"-> Tour_sped
    | "UPS"-> Ups
    | "UPS_A_GEB"-> Ups_a_geb
    | "UPS_CH"-> Ups_ch
    | "WERKVK"-> Werkvk
    | _ -> failwith ("invalid deliverer code: " ^ str)

let to_int deliverer = 
    match deliverer with
    | Abholer -> 0
    | Abholung -> 1
    | Auslfa -> 2
    | Dhl -> 3
    | Infehler -> 4
    | Kep -> 5
    | Meyerjumb -> 6
    | Post -> 7
    | Sped -> 8
    | Speddsv -> 9
    | Sped_osna -> 10
    | Tour_sped -> 11
    | Ups -> 12
    | Ups_a_geb -> 13
    | Ups_ch -> 14
    | Werkvk -> 15

let of_int n = 
    match n with
    | 0 -> Abholer
    | 1 -> Abholung
    | 2 -> Auslfa
    | 3 -> Dhl
    | 4 -> Infehler
    | 5 -> Kep
    | 6 -> Meyerjumb
    | 7 -> Post
    | 8 -> Sped
    | 9 -> Speddsv
    | 10 -> Sped_osna
    | 11 -> Tour_sped
    | 12 -> Ups
    | 13 -> Ups_a_geb
    | 14 -> Ups_ch
    | 15 -> Werkvk
    | _ -> failwith "invalid deliverer code"

let to_list deliverer = 
    let idx = to_int deliverer in
    List.init 16 ~f:(fun i -> if i = idx then 1.0 else 0.0)
