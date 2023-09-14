open Core
open Owl_plplot
open Owl

let print_array arr = 
    let length = Array.length arr in
    for i = 0 to length - 1 do 
        printf "%f\n" arr.(i)
    done

let histogram x name = 
    let h = Plot.create ~m:1 ~n:1 name in
    Plot.subplot h 0 0;
    Plot.set_title h "histogram";
    let x' = Mat.of_array x 1 (Array.length x) in
    Plot.histogram ~bin:20 ~h x';
    Plot.output h

let basic_plot x labels name =
    let x' = Mat.of_array x 1 (Array.length x) in
    let h = Plot.create ~m:1 ~n:1 name in
    Plot.subplot h 0 0;
    Plot.set_title h "damage ratios";
    Plot.bar x';
    Plot.legend_on h labels;
    Plot.output h
