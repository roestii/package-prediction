open Core 

type t = 
    | Abschluss
    | Anleitung
    | Bediensch
    | Befestigun
    | Buersten
    | Dichtungen
    | Endkappen
    | Etiketten
    | Faltrollo
    | Federn
    | Fvorhang
    | Fuehrungspr
    | Getriebe
    | Holzprof
    | Inschutz
    | Jalousie
    | Kartons
    | Keder
    | Ketten
    | Klebebaende
    | Klett
    | Kollektion
    | Kopfprof
    | Kordeln
    | Lacke
    | Lamelle
    | Lamellenvo
    | Leihmesses
    | Massiv
    | Motoren
    | Muttern
    | Papprohe
    | Plissee_20
    | Plissee_wa
    | Pospraes
    | Ppshop
    | Produktbau
    | Produktion
    | Prospekte
    | Praesenter
    | Pruefung
    | Produktgruppe
    | Reparatur
    | Rollen
    | Rollo
    | Rollwagen
    | Rundrohr
    | Scheiben
    | Schnur
    | Schrauben
    | Schreibwar
    | Shutters
    | Sonderanfe
    | Sonstige
    | Stifte
    | Variorollo
    | Verpackung
    | Vorhaenge
    | Werbemitte
    | Zubehoer
    | Zubehoerbeu
[@@deriving show]


let of_string str = 
    match str with 
    | "ABSCHLUSS" -> Abschluss
    | "ANLEITUNG" -> Anleitung
    | "BEDIENSCH" -> Bediensch
    | "BEFESTIGUN" -> Befestigun
    | "BÜRSTEN" -> Buersten
    | "DICHTUNGEN" -> Dichtungen
    | "ENDKAPPEN" -> Endkappen
    | "ETIKETTEN" -> Etiketten
    | "FALTROLLO" -> Faltrollo
    | "FEDERN" -> Federn
    | "FVORHANG" -> Fvorhang
    | "FÜHRUNGSPR" -> Fuehrungspr
    | "GETRIEBE" -> Getriebe
    | "HOLZPROF" -> Holzprof
    | "INSCHUTZ" -> Inschutz
    | "JALOUSIE" -> Jalousie
    | "KARTONS" -> Kartons
    | "KEDER" -> Keder
    | "KETTEN" -> Ketten
    | "KLEBEBÄNDE" -> Klebebaende
    | "KLETT" -> Klett
    | "KOLLEKTION" -> Kollektion
    | "KOPFPROF" -> Kopfprof
    | "KORDELN" -> Kordeln
    | "LACKE" -> Lacke
    | "LAMELLE" -> Lamelle
    | "LAMELLENVO" -> Lamellenvo
    | "LEIHMESSES" -> Leihmesses
    | "MASSIV" -> Massiv
    | "MOTOREN" -> Motoren
    | "MUTTERN" -> Muttern
    | "PAPPROHE" -> Papprohe
    | "PLISSEE_20" -> Plissee_20
    | "PLISSEE_WA" -> Plissee_wa
    | "POS-PRÄS" -> Pospraes
    | "PP-SHOP" -> Ppshop
    | "PRODUKTBAU" -> Produktbau
    | "PRODUKTION" -> Produktion
    | "PROSPEKTE" -> Prospekte
    | "PRÄSENTER" -> Praesenter
    | "PRÜFUNG" -> Pruefung
    | "REPARATUR" -> Reparatur
    | "ROLLEN" -> Rollen
    | "ROLLO" -> Rollo
    | "ROLLWAGEN" -> Rollwagen
    | "RUNDROHR" -> Rundrohr
    | "SCHEIBEN" -> Scheiben
    | "SCHNUR" -> Schnur
    | "SCHRAUBEN" -> Schrauben
    | "SCHREIBWAR" -> Schreibwar
    | "SHUTTERS" -> Shutters
    | "SONDERANFE" -> Sonderanfe
    | "SONSTIGE" -> Sonstige
    | "STIFTE" -> Stifte
    | "VARIOROLLO" -> Variorollo
    | "VERPACKUNG" -> Verpackung
    | "VORHÄNGE" -> Vorhaenge
    | "WERBEMITTE" -> Werbemitte
    | "ZUBEHÖR" -> Zubehoer
    | "ZUBEHÖRBEU" -> Zubehoerbeu
    | _ -> failwith "invalid article type"

let rec articles_of_group articles group = 
    match group with 
    | [] -> articles
    | hd :: tail -> 
        let article = of_string hd.(19) in
        let amount = Float.of_string hd.(7) in

        let count = match List.Assoc.find ~equal:phys_equal articles article with 
        | None -> 0.0
        | Some (x) -> x in

        articles_of_group (List.Assoc.add ~equal:phys_equal articles article (count +. amount)) tail
