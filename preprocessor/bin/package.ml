open Core 
open Package_t

type t = {
    db_nr: string;
    pkg_nr: int;
    cst_nr: int;
    articles: (Article.t * float) list; 
    weight: float;
    size: float;
    lat: float;
    lon: float;
    deliverer: Deliverer.t;
    country: Country.t;
    plz: string;
    is_damaged: bool;
} [@@deriving show]

let of_package_j (package_j: package) =
    let articles = List.map package_j.articles ~f:(fun (article, amount) -> 
        ((Article.of_string article), amount)) in
    let country = Country.of_string package_j.location.country in
    let deliverer = Deliverer.of_string package_j.deliverer in

    {   db_nr = package_j.db_nr;
        pkg_nr = 1;
        size = package_j.size;
        weight = package_j.weight;
        articles;
        country;
        deliverer;
        cst_nr = package_j.customer_nr;
        lat = package_j.location.lat;
        lon = package_j.location.lon;
        plz = package_j.location.postal;
        is_damaged = package_j.is_damaged;
    }

let to_list package = 
    let articles = Article.to_list package.articles in
    let country = Country.to_list package.country in
    let deliverer = Deliverer.to_list package.deliverer in
    (*let cst_nr = Float.of_int package.cst_nr in
    let is_damaged = if package.is_damaged then 1.0 else 0.0 in*)

    (package.weight :: package.size :: package.lon :: package.lat :: []) @ country @ deliverer @ articles @ []

let of_group group = 
    let open Float.O in
    let hd = Option.value_exn ~message:"empty group" (List.hd group) in
    let db_nr = hd.(1) in
    let cst_nr = Int.of_string hd.(16) in
    let weight = List.fold ~init:0.0 ~f:(fun acc el -> 
        let weight = Float.of_string el.(8) in
        if weight > acc then weight else acc) group in
    let size = List.fold ~init:0.0 ~f:(fun acc el -> 
        let size = Float.of_string el.(9) in
        if size > acc then size else acc) group in
    let country = Country.of_string hd.(17) in
    let plz = hd.(18) in
    let deliverer = Deliverer.of_string hd.(20) in
    let articles = Article.articles_of_group [] group in
    let is_damaged = String.equal hd.(23) "ja" in

    {   db_nr;
        cst_nr;
        pkg_nr = 1;
        weight;
        size;
        country;
        lat = 0.;
        lon = 0.;
        plz;
        deliverer;
        articles;
        is_damaged;
    }

