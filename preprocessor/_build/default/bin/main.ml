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

(*let print_packages lst = 
    List.iter ~f:(fun el -> printf "%s\n" (Package.show el)) lst*)

let rec _damage_ratio n res vec_reprs =
    match vec_reprs with 
    | [] -> res 
    | (repr, damaged) :: tail -> 
        let el = List.nth_exn repr n in
        if (Float.compare el 0.0) > 0 && damaged then 
            let (d, nd) = res in 
            _damage_ratio n (d + 1, nd) tail
        else if (Float.compare el 0.0) > 0 && (not damaged) then 
            let (d, nd) = res in
            _damage_ratio n (d, nd + 1) tail
        else 
            _damage_ratio n res tail

let _print_ratios ratios = 
    List.iter ~f:(fun (d, nd) -> 
        printf "%d;%d\n" d nd) ratios

let write_country_postal packages filename = 
    let data = List.fold ~init:[] ~f:(fun acc (el: Package.t) -> 
        let entries = List.map ~f:(fun (article, amount) -> 
            (Country.to_string el.country) :: el.plz :: (Article.to_string article) :: (Float.to_string amount) :: []) el.articles in
        entries @ acc
        ) packages in 
    let arr = Array.of_list (List.map ~f:Array.of_list data) in
    Owl_io.write_csv ~sep:',' arr filename

let () = 
    let file_path = "../data/Rohdaten für DVO-Projekt 2022.csv" in
    let data = Owl_io.read_csv ~sep:',' file_path in
    let data = Array.slice data 1 (Array.length data) in
    let groups = groups (Array.to_list data) [] in 
    let groups = List.filter ~f:is_one_package groups in
    let packages = List.map ~f:Package.of_group groups in
    (*let reprs = List.map ~f:(fun el -> 
        let article_repr = Article.to_list el.articles in
        (article_repr, el.is_damaged)) packages in

    let ratios = List.init 60 ~f:(fun n -> damage_ratio n (0, 0) reprs) in 
    print_ratios ratios;*)

    (*let reprs = List.map ~f:(fun el -> 
        let deliverer_repr = Deliverer.to_list el.deliverer in
        (deliverer_repr, el.is_damaged)) packages in
    let ratios = List.init 16 ~f:(fun n -> damage_ratio n (0, 0) reprs) in 
    printf "Deliverer ratios \n\n";
    print_ratios ratios;*)

    (*let reprs = List.map ~f:(fun el -> 
        let country_repr = Country.to_list el.country in
        (country_repr, el.is_damaged)) packages in
    let ratios = List.init 30 ~f:(fun n -> damage_ratio n (0, 0) reprs) in 
    printf "Country ratios \n\n";
    print_ratios ratios;*)

    (*let ratios = List.map ~f:(fun (d, nd) -> 
        let d = Float.of_int d in
        let nd = Float.of_int nd in
        (d *. 1000.0) /. (d +. nd)) ratios in

    let labels = List.init 30 ~f:(fun n -> Country.of_int n) in
    Plotting.basic_plot (Array.of_list ratios) (Array.of_list labels) "article_damage_ratios.png";*)

    (* write tha resulting vec reprs out to the out.csv file
    let csv_data = List.map ~f:(fun el -> 
    let vec_reprs = List.map ~f:(fun el -> Float.to_string el) (Package.to_list el) in
    let lst = el.db_nr :: vec_reprs in
    Array.of_list lst) packages in
    let arr = Array.of_list csv_data in
    Owl_io.write_csv ~sep:',' arr "out.csv";*)

    (* json vec repr creation of packages -> out.jsonl
        let vec_reprs = List.map ~f:(fun el -> 
        let vec_repr = List.map ~f:(fun el -> `Float el) (Package.to_list el) in
        let package: (Yojson.t) = `Assoc [
            ("db_nr", `String el.db_nr);
            ("vec_repr", `List vec_repr);
        ] in 
        Yojson.to_string package) packages in
    
    Out_channel.write_lines "out.jsonl" vec_reprs;*)

    (* weight based histogram of damaged packages*)
    let damaged_packages = List.filter ~f:(fun el -> el.is_damaged) packages in
    write_country_postal damaged_packages "things.csv";
    (*printf "Damaged packages: %d" (List.length damaged_packages);*)
    (*let weights = List.map ~f:(fun el -> el.weight) damaged_packages in
    let weights = Array.of_list weights in
    Plotting.histogram weights "weights_histogram_damaged_packages_20_bins.png";*)
    ()
