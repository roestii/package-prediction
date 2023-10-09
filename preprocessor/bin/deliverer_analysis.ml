open Core

type entry = {
    place: string;
    deliverer: string;
    is_damaged: bool;
} [@@deriving show]

let _print_list lst = 
    List.iter ~f:(fun el -> print_endline (show_entry el)) lst

let rec to_del_dist lst n res = 
    match lst with 
    | [] -> res 
    | (d, nd) :: tail -> 
        let deliverer = Deliverer.of_int n |> Deliverer.to_string in
        let assoc = `Assoc [
            ("deliverer", `String deliverer);
            ("damaged", `Int d);
            ("not_damaged", `Int nd);
        ] in
            
        to_del_dist tail (n + 1) (assoc :: res)

let () = 
    let out_filename = "../data/deliverer_distributions.jsonl" in
    let filename = "../data/full_locations_with_names.jsonl" in
    let content = In_channel.read_lines filename in
    let entries = List.fold ~init:[] ~f:(fun acc el ->
        let open Yojson.Basic.Util in
        let entry = Yojson.Basic.from_string el in
        let name = entry 
            |> member "location" 
            |> member "name" 
            |> to_string in

        let places = String.split ~on:',' name |> List.rev in
        let place = match List.length places with 
        | n when n > 3 -> List.nth_exn places 3 |> String.strip |> Option.some
        | n when n > 2 -> List.nth_exn places 2 |> String.strip |> Option.some
        | _ -> None in

        match place with 
        | None -> acc
        | Some (place) ->
            let deliverer = entry |> member "deliverer" |> to_string in
            let is_damaged = entry |> member "is_damaged" |> to_bool in

            let arr = match List.Assoc.find ~equal:String.equal acc place with 
            | None -> Array.init 16 ~f:(fun _ -> (0, 0)) 
            | Some (arr) -> arr in

            let idx = Deliverer.of_string deliverer 
                |> Deliverer.to_int in

            let (d, nd) = arr.(idx) in
            let (d, nd) = if is_damaged then (d + 1, nd) else (d, nd + 1) in
            arr.(idx) <- (d, nd);

            List.Assoc.add ~equal:String.equal acc place arr
    ) content in

    let lines = List.map ~f:(fun (key, value) ->
        let values = List.of_array value in
        let del_dist = `List (to_del_dist values 0 []) in

        let obj = `Assoc [
            ("place", `String key);
            ("del_dist", del_dist);
        ] in

        Yojson.to_string obj
    ) entries in

    Out_channel.write_lines out_filename lines;

