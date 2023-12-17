open Core

let is_damaged line = 
    let open Yojson.Basic.Util in
    let package = Yojson.Basic.from_string line in
    let is_damaged = phys_equal (package |> member "is_damaged" |> to_int) 1 in
    is_damaged

let every_nth lst ~n =
    let rec every_nth' lst n idx res leftover = 
        match lst with 
        | [] -> (res, leftover)
        | hd :: tail -> 
            (if phys_equal (idx % n)  0 then
                every_nth' tail n (idx + 1) (hd :: res) leftover
            else 
                every_nth' tail n (idx + 1) res (hd :: leftover)) in
    every_nth' lst n 0 [] []


let () = 
    let filename = "../data/dataset_base.jsonl" in
    let outfile_cutted = "../data/cutted.jsonl" in
    let outfile_leftover = "../data/dataset_without_cutted.jsonl" in

    let lines = In_channel.read_lines filename in
    let damaged = List.filter lines ~f:is_damaged in
    let not_damaged = List.filter lines ~f:(fun el -> not (is_damaged el)) in

    let every_twelth = every_nth ~n:12 in
    let (cutted_d, leftover_d) = every_twelth damaged in
    let (cutted_nd, leftover_nd) = every_twelth not_damaged in

    let cutted = cutted_d @ cutted_nd in
    let leftover = leftover_d @ leftover_nd in

    Out_channel.write_lines outfile_cutted cutted;
    Out_channel.write_lines outfile_leftover leftover;
    
