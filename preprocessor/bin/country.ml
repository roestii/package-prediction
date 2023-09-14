open Core 

type t = 
    | AT
    | AU
    | BE
    | BG
    | BH
    | CA
    | CH
    | CZ
    | DE
    | DK
    | EE
    | ES
    | FR
    | GE
    | GR
    | HR
    | HU
    | IE
    | IT
    | LI
    | LU
    | MG
    | MT
    | NL
    | NZ
    | PT
    | RO
    | RS
    | SE
    | SI
[@@deriving show]

let of_string str = 
    match str with 
    | "AT" -> AT
    | "AU" -> AU
    | "BE" -> BE
    | "BG" -> BG
    | "BH" -> BH
    | "CA" -> CA
    | "CH" -> CH
    | "CZ" -> CZ
    | "DE" -> DE
    | "DK" -> DK
    | "EE" -> EE
    | "ES" -> ES
    | "FR" -> FR
    | "GE" -> GE
    | "GR" -> GR
    | "HR" -> HR
    | "HU" -> HU
    | "IE" -> IE
    | "IT" -> IE
    | "LI" -> LI
    | "LU" -> LU
    | "MG" -> MG
    | "MT" -> MT
    | "NL" -> NL
    | "NZ" -> NZ
    | "PT" -> PT
    | "RO" -> RO
    | "RS" -> RS
    | "SE" -> SE
    | "SI" -> SI
    | _ -> failwith ("invalid country code: " ^ str)

let to_int country = 
    match country with
    | AT -> 0
    | AU -> 1
    | BE -> 2
    | BG -> 3
    | BH -> 4
    | CA -> 5
    | CH -> 6
    | CZ -> 7
    | DE -> 8
    | DK -> 9
    | EE -> 10
    | ES -> 11
    | FR -> 12
    | GE -> 13
    | GR -> 14
    | HR -> 15
    | HU -> 16
    | IE -> 17
    | IT -> 18
    | LI -> 19
    | LU -> 20
    | MG -> 21
    | MT -> 22
    | NL -> 23
    | NZ -> 24
    | PT -> 25
    | RO -> 26
    | RS -> 27
    | SE -> 28
    | SI -> 29

let to_string country = 
    match country with
    | AT -> "AT"
    | AU -> "AU"
    | BE -> "BE"
    | BG -> "BG"
    | BH -> "BH"
    | CA -> "CA"
    | CH -> "CH"
    | CZ -> "CZ"
    | DE -> "DE"
    | DK -> "DK"
    | EE -> "EE"
    | ES -> "ES"
    | FR -> "FR"
    | GE -> "GE"
    | GR -> "GR"
    | HR -> "HR"
    | HU -> "HU"
    | IE -> "IE"
    | IT -> "IT"
    | LI -> "LI"
    | LU -> "LU"
    | MG -> "MG"
    | MT -> "MT"
    | NL -> "NL"
    | NZ -> "NZ"
    | PT -> "PT"
    | RO -> "RO"
    | RS -> "RS"
    | SE -> "SE"
    | SI -> "SI"

let of_int n = 
    match n with
    | 0 -> AT
    | 1 -> AU
    | 2 -> BE
    | 3 -> BG
    | 4 -> BH
    | 5 -> CA
    | 6 -> CH
    | 7 -> CZ
    | 8 -> DE
    | 9 -> DK
    | 10 -> EE
    | 11 -> ES
    | 12 -> FR
    | 13 -> GE
    | 14 -> GR
    | 15 -> HR
    | 16 -> HU
    | 17 -> IE
    | 18 -> IT
    | 19 -> LI
    | 20 -> LU
    | 21 -> MG
    | 22 -> MT
    | 23 -> NL
    | 24 -> NZ
    | 25 -> PT
    | 26 -> RO
    | 27 -> RS
    | 28 -> SE
    | 29 -> SI
    | _ -> failwith "invalid country code"

let to_list country = 
    let idx = to_int country in
    List.init 30 ~f:(fun i -> if i = idx then 1.0 else 0.0)
