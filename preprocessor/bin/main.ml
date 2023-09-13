open Core

let rec groups lines res = 
    match lines with 
    | [] -> res
    | hd :: rest -> 
        (let ls_nr = hd.(1) in
        match res with 
        | [] -> groups rest [[hd]]
        | first_group :: tail ->
            match List.hd first_group with 
            | Some (first) -> 
                if String.equal first.(1) ls_nr then 
                    groups rest ((hd :: first_group) :: tail)                    
                else 
                    groups rest ([hd] :: res)
            | None -> failwith "unreachable")

(*let print_groups groups = 
    List.iter groups ~f:(fun group ->
        let _ = print_endline "New group" in
        let _ = List.iter group ~f:(fun entry ->
            let listed = Array.to_list entry in
            let concatenated = String.concat ~sep:" " listed in
            printf "%s\n" concatenated) in
        print_endline "End group\n\n")*)

(*let print_types types = 
    List.iter types ~f:(fun el -> print_endline el)*)

let is_one_package group = 
    let nums = List.map group ~f:(fun el -> Int.of_string el.(3)) in
    let sum = List.fold ~init:0 ~f:(+) nums in
    let len = List.length group in
    sum = len

let print_packages lst = 
    List.iter ~f:(fun el -> printf "%s\n" (Package.show el)) lst

let () = 
    let file_path = "../data/Rohdaten für DVO-Projekt 2022.csv" in
    let data = Owl_io.read_csv ~sep:',' file_path in
    let data = Array.slice data 1 (Array.length data) in
    let groups = groups (Array.to_list data) [] in 
    let groups = List.filter ~f:is_one_package groups in
    print_endline "got groups";
    let packages = List.map ~f:Package.of_group groups in
    print_packages packages
    (*let _ = print_groups groups in*)
