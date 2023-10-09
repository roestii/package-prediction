open Core

type entry = {
    name: string;
    is_damaged: bool;
} [@@deriving show]

let _print_list lst = 
    List.iter ~f:(fun el -> print_endline (show_entry el)) lst

let () = 
    let filename = "../data/full_locations_with_names.jsonl" in
    let _out_filename = "../data/location_occurence_map.jsonl" in

    let lines = In_channel.read_lines filename in
    let places = List.map ~f:(fun el -> 
        let open Yojson.Basic.Util in
        let package = Yojson.Basic.from_string el in
        let name = package |> member "location" |> member "name" |> to_string in
        let is_damaged = package |> member "is_damaged" |> to_bool in

        {name; is_damaged}
    ) lines in

    let occurence_map = List.fold ~init:[] ~f:(fun acc el -> 
        let areas = List.rev (String.split ~on:',' el.name) in
        match List.nth areas 3 with 
        | Some (x) -> 
            let x = String.strip x in
            let (dc, ndc) = match List.Assoc.find ~equal:String.equal acc x with 
            | None -> (0, 0)
            | Some ((dc, ndc)) -> (dc, ndc) in
            
            let (dc, ndc) = if el.is_damaged then (dc + 1, ndc) else (dc, ndc + 1) in
            List.Assoc.add ~equal:String.equal acc x (dc, ndc)
        | None -> acc
    ) places in

    let max = List.fold ~init:0.0 ~f:(fun acc (_, (dc, ndc)) -> 
        let dc = Float.of_int dc in
        let ndc = Float.of_int ndc in
        let ratio = dc /. (dc +. ndc) in

        let open Float.O in
        if ratio > acc then ratio else acc
    ) occurence_map in

    printf "%f" max;

    (*let mapped = List.map ~f:(fun (key, (dc, ndc)) -> 
        let assoc = `Assoc [
            ("place", `String key);
            ("counts", `Assoc [
                ("dc", `Int dc);
                ("ndc", `Int ndc);
            ])
        ] in
        Yojson.to_string assoc
    ) occurence_map in

    Out_channel.write_lines out_filename mapped;*)

    (*print_list places;
    print_endline (List.nth_exn occurence_map 0);*)
    ()

