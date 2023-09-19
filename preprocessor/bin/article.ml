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

let to_string article = 
    match article with 
    | Abschluss -> "ABSCHLUSS" 
    | Anleitung -> "ANLEITUNG" 
    | Bediensch -> "BEDIENSCH" 
    | Befestigun -> "BEFESTIGUN" 
    | Buersten -> "BÜRSTEN" 
    | Dichtungen -> "DICHTUNGEN" 
    | Endkappen -> "ENDKAPPEN" 
    | Etiketten -> "ETIKETTEN" 
    | Faltrollo -> "FALTROLLO" 
    | Federn -> "FEDERN" 
    | Fvorhang -> "FVORHANG" 
    | Fuehrungspr -> "FÜHRUNGSPR" 
    | Getriebe -> "GETRIEBE" 
    | Holzprof -> "HOLZPROF" 
    | Inschutz -> "INSCHUTZ" 
    | Jalousie -> "JALOUSIE" 
    | Kartons -> "KARTONS" 
    | Keder -> "KEDER" 
    | Ketten -> "KETTEN" 
    | Klebebaende -> "KLEBEBÄNDE" 
    | Klett -> "KLETT" 
    | Kollektion -> "KOLLEKTION" 
    | Kopfprof -> "KOPFPROF" 
    | Kordeln -> "KORDELN" 
    | Lacke -> "LACKE" 
    | Lamelle -> "LAMELLE" 
    | Lamellenvo -> "LAMELLENVO" 
    | Leihmesses -> "LEIHMESSES" 
    | Massiv -> "MASSIV" 
    | Motoren -> "MOTOREN" 
    | Muttern -> "MUTTERN" 
    | Papprohe -> "PAPPROHE" 
    | Plissee_20 -> "PLISSEE_20" 
    | Plissee_wa -> "PLISSEE_WA" 
    | Pospraes -> "POS-PRÄS" 
    | Ppshop -> "PP-SHOP" 
    | Produktbau -> "PRODUKTBAU" 
    | Produktion -> "PRODUKTION" 
    | Prospekte -> "PROSPEKTE" 
    | Praesenter -> "PRÄSENTER" 
    | Pruefung -> "PRÜFUNG" 
    | Reparatur -> "REPARATUR" 
    | Rollen -> "ROLLEN" 
    | Rollo -> "ROLLO" 
    | Rollwagen -> "ROLLWAGEN" 
    | Rundrohr -> "RUNDROHR" 
    | Scheiben -> "SCHEIBEN" 
    | Schnur -> "SCHNUR" 
    | Schrauben -> "SCHRAUBEN" 
    | Schreibwar -> "SCHREIBWAR" 
    | Shutters -> "SHUTTERS" 
    | Sonderanfe -> "SONDERANFE" 
    | Sonstige -> "SONSTIGE" 
    | Stifte -> "STIFTE" 
    | Variorollo -> "VARIOROLLO" 
    | Verpackung -> "VERPACKUNG" 
    | Vorhaenge -> "VORHÄNGE" 
    | Werbemitte -> "WERBEMITTE" 
    | Zubehoer -> "ZUBEHÖR" 
    | Zubehoerbeu -> "ZUBEHÖRBEU" 

let to_int article = 
    match article with
    | Abschluss -> 0
    | Anleitung -> 1
    | Bediensch -> 2
    | Befestigun -> 3
    | Buersten -> 4
    | Dichtungen -> 5
    | Endkappen -> 6
    | Etiketten -> 7
    | Faltrollo -> 8
    | Federn -> 9
    | Fvorhang -> 10
    | Fuehrungspr -> 11
    | Getriebe -> 12
    | Holzprof -> 13
    | Inschutz -> 14
    | Jalousie -> 15
    | Kartons -> 16
    | Keder -> 17
    | Ketten -> 18
    | Klebebaende -> 19
    | Klett -> 20
    | Kollektion -> 21
    | Kopfprof -> 22
    | Kordeln -> 23
    | Lacke -> 24
    | Lamelle -> 25
    | Lamellenvo -> 26
    | Leihmesses -> 27
    | Massiv -> 28
    | Motoren -> 29
    | Muttern -> 30
    | Papprohe -> 31
    | Plissee_20 -> 32
    | Plissee_wa -> 33
    | Pospraes -> 34
    | Ppshop -> 35
    | Produktbau -> 36
    | Produktion -> 37
    | Prospekte -> 38
    | Praesenter -> 39
    | Pruefung -> 40
    | Reparatur -> 41
    | Rollen -> 42
    | Rollo -> 43
    | Rollwagen -> 44
    | Rundrohr -> 45
    | Scheiben -> 46
    | Schnur -> 47
    | Schrauben -> 48
    | Schreibwar -> 49
    | Shutters -> 50
    | Sonderanfe -> 51
    | Sonstige -> 52
    | Stifte -> 53
    | Variorollo -> 54
    | Verpackung -> 55
    | Vorhaenge -> 56
    | Werbemitte -> 57
    | Zubehoer -> 58
    | Zubehoerbeu -> 59

let of_int n = 
    match n with
    | 0 -> Abschluss
    | 1 -> Anleitung
    | 2 -> Bediensch
    | 3 -> Befestigun
    | 4 -> Buersten
    | 5 -> Dichtungen
    | 6 -> Endkappen
    | 7 -> Etiketten
    | 8 -> Faltrollo
    | 9 -> Federn
    | 10 -> Fvorhang
    | 11 -> Fuehrungspr
    | 12 -> Getriebe
    | 13 -> Holzprof
    | 14 -> Inschutz
    | 15 -> Jalousie
    | 16 -> Kartons
    | 17 -> Keder
    | 18 -> Ketten
    | 19 -> Klebebaende
    | 20 -> Klett
    | 21 -> Kollektion
    | 22 -> Kopfprof
    | 23 -> Kordeln
    | 24 -> Lacke
    | 25 -> Lamelle
    | 26 -> Lamellenvo
    | 27 -> Leihmesses
    | 28 -> Massiv
    | 29 -> Motoren
    | 30 -> Muttern
    | 31 -> Papprohe
    | 32 -> Plissee_20
    | 33 -> Plissee_wa
    | 34 -> Pospraes
    | 35 -> Ppshop
    | 36 -> Produktbau
    | 37 -> Produktion
    | 38 -> Prospekte
    | 39 -> Praesenter
    | 40 -> Pruefung
    | 41 -> Reparatur
    | 42 -> Rollen
    | 43 -> Rollo
    | 44 -> Rollwagen
    | 45 -> Rundrohr
    | 46 -> Scheiben
    | 47 -> Schnur
    | 48 -> Schrauben
    | 49 -> Schreibwar
    | 50 -> Shutters
    | 51 -> Sonderanfe
    | 52 -> Sonstige
    | 53 -> Stifte
    | 54 -> Variorollo
    | 55 -> Verpackung
    | 56 -> Vorhaenge
    | 57 -> Werbemitte
    | 58 -> Zubehoer
    | 59 -> Zubehoerbeu
    | _ -> failwith "invalid digit for article type"

let to_list articles = 
    let empty = Array.init 60 ~f:(fun _ -> 0.0) in
    let arr = List.fold ~init:empty ~f:(fun acc (article, amount) -> 
        let idx = to_int article in
        acc.(idx) <- acc.(idx) +. amount;
        acc
        ) articles in
    Array.to_list arr

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
