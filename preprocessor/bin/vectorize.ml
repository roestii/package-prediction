open Core
open Package_j

let _print_list lst = 
    List.iter lst ~f:(fun el -> printf "%f\n" el)

let () = 
    let filename = "../data/full_locations_updated_tupl_repr.jsonl" in
    let lines = In_channel.read_lines filename in
    let packages = List.map lines ~f:package_of_string in
    let packages = List.map packages ~f:Package.of_package_j in
    let vec_reprs = List.map packages ~f:(fun el -> 
        let vec_repr = Package.to_list el in
        let vec_repr = List.map vec_repr ~f:(fun el -> `Float el) in
        let is_damaged = if el.is_damaged then 1 else 0 in
        let assoc = `Assoc [
            ("db_nr", `String el.db_nr);
            ("vec_repr", `List vec_repr);
            ("is_damaged", `Int is_damaged)
        ] in
        Yojson.to_string assoc) in

    let out_file = "../data/dataset_with_locations.jsonl" in
    Out_channel.write_lines out_file vec_reprs;
    ()
