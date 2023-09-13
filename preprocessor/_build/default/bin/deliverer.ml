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
