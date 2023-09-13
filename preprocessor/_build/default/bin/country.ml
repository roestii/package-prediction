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

