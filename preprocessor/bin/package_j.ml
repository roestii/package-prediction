(* Auto-generated from "package.atd" *)
[@@@ocaml.warning "-27-32-33-35-39"]

type location = Package_t.location = {
  country: string;
  postal: string;
  lat: float;
  lon: float
}

type package = Package_t.package = {
  db_nr: string;
  customer_nr: int;
  articles: (string * float) list;
  weight: float;
  size: float;
  location: location;
  deliverer: string;
  is_damaged: bool
}

let write_location : _ -> location -> _ = (
  fun ob (x : location) ->
    Buffer.add_char ob '{';
    let is_first = ref true in
    if !is_first then
      is_first := false
    else
      Buffer.add_char ob ',';
      Buffer.add_string ob "\"country\":";
    (
      Yojson.Safe.write_string
    )
      ob x.country;
    if !is_first then
      is_first := false
    else
      Buffer.add_char ob ',';
      Buffer.add_string ob "\"postal\":";
    (
      Yojson.Safe.write_string
    )
      ob x.postal;
    if !is_first then
      is_first := false
    else
      Buffer.add_char ob ',';
      Buffer.add_string ob "\"lat\":";
    (
      Yojson.Safe.write_float
    )
      ob x.lat;
    if !is_first then
      is_first := false
    else
      Buffer.add_char ob ',';
      Buffer.add_string ob "\"lon\":";
    (
      Yojson.Safe.write_float
    )
      ob x.lon;
    Buffer.add_char ob '}';
)
let string_of_location ?(len = 1024) x =
  let ob = Buffer.create len in
  write_location ob x;
  Buffer.contents ob
let read_location = (
  fun p lb ->
    Yojson.Safe.read_space p lb;
    Yojson.Safe.read_lcurl p lb;
    let field_country = ref (None) in
    let field_postal = ref (None) in
    let field_lat = ref (None) in
    let field_lon = ref (None) in
    try
      Yojson.Safe.read_space p lb;
      Yojson.Safe.read_object_end lb;
      Yojson.Safe.read_space p lb;
      let f =
        fun s pos len ->
          if pos < 0 || len < 0 || pos + len > String.length s then
            invalid_arg (Printf.sprintf "out-of-bounds substring position or length: string = %S, requested position = %i, requested length = %i" s pos len);
          match len with
            | 3 -> (
                if String.unsafe_get s pos = 'l' then (
                  match String.unsafe_get s (pos+1) with
                    | 'a' -> (
                        if String.unsafe_get s (pos+2) = 't' then (
                          2
                        )
                        else (
                          -1
                        )
                      )
                    | 'o' -> (
                        if String.unsafe_get s (pos+2) = 'n' then (
                          3
                        )
                        else (
                          -1
                        )
                      )
                    | _ -> (
                        -1
                      )
                )
                else (
                  -1
                )
              )
            | 6 -> (
                if String.unsafe_get s pos = 'p' && String.unsafe_get s (pos+1) = 'o' && String.unsafe_get s (pos+2) = 's' && String.unsafe_get s (pos+3) = 't' && String.unsafe_get s (pos+4) = 'a' && String.unsafe_get s (pos+5) = 'l' then (
                  1
                )
                else (
                  -1
                )
              )
            | 7 -> (
                if String.unsafe_get s pos = 'c' && String.unsafe_get s (pos+1) = 'o' && String.unsafe_get s (pos+2) = 'u' && String.unsafe_get s (pos+3) = 'n' && String.unsafe_get s (pos+4) = 't' && String.unsafe_get s (pos+5) = 'r' && String.unsafe_get s (pos+6) = 'y' then (
                  0
                )
                else (
                  -1
                )
              )
            | _ -> (
                -1
              )
      in
      let i = Yojson.Safe.map_ident p f lb in
      Atdgen_runtime.Oj_run.read_until_field_value p lb;
      (
        match i with
          | 0 ->
            field_country := (
              Some (
                (
                  Atdgen_runtime.Oj_run.read_string
                ) p lb
              )
            );
          | 1 ->
            field_postal := (
              Some (
                (
                  Atdgen_runtime.Oj_run.read_string
                ) p lb
              )
            );
          | 2 ->
            field_lat := (
              Some (
                (
                  Atdgen_runtime.Oj_run.read_number
                ) p lb
              )
            );
          | 3 ->
            field_lon := (
              Some (
                (
                  Atdgen_runtime.Oj_run.read_number
                ) p lb
              )
            );
          | _ -> (
              Yojson.Safe.skip_json p lb
            )
      );
      while true do
        Yojson.Safe.read_space p lb;
        Yojson.Safe.read_object_sep p lb;
        Yojson.Safe.read_space p lb;
        let f =
          fun s pos len ->
            if pos < 0 || len < 0 || pos + len > String.length s then
              invalid_arg (Printf.sprintf "out-of-bounds substring position or length: string = %S, requested position = %i, requested length = %i" s pos len);
            match len with
              | 3 -> (
                  if String.unsafe_get s pos = 'l' then (
                    match String.unsafe_get s (pos+1) with
                      | 'a' -> (
                          if String.unsafe_get s (pos+2) = 't' then (
                            2
                          )
                          else (
                            -1
                          )
                        )
                      | 'o' -> (
                          if String.unsafe_get s (pos+2) = 'n' then (
                            3
                          )
                          else (
                            -1
                          )
                        )
                      | _ -> (
                          -1
                        )
                  )
                  else (
                    -1
                  )
                )
              | 6 -> (
                  if String.unsafe_get s pos = 'p' && String.unsafe_get s (pos+1) = 'o' && String.unsafe_get s (pos+2) = 's' && String.unsafe_get s (pos+3) = 't' && String.unsafe_get s (pos+4) = 'a' && String.unsafe_get s (pos+5) = 'l' then (
                    1
                  )
                  else (
                    -1
                  )
                )
              | 7 -> (
                  if String.unsafe_get s pos = 'c' && String.unsafe_get s (pos+1) = 'o' && String.unsafe_get s (pos+2) = 'u' && String.unsafe_get s (pos+3) = 'n' && String.unsafe_get s (pos+4) = 't' && String.unsafe_get s (pos+5) = 'r' && String.unsafe_get s (pos+6) = 'y' then (
                    0
                  )
                  else (
                    -1
                  )
                )
              | _ -> (
                  -1
                )
        in
        let i = Yojson.Safe.map_ident p f lb in
        Atdgen_runtime.Oj_run.read_until_field_value p lb;
        (
          match i with
            | 0 ->
              field_country := (
                Some (
                  (
                    Atdgen_runtime.Oj_run.read_string
                  ) p lb
                )
              );
            | 1 ->
              field_postal := (
                Some (
                  (
                    Atdgen_runtime.Oj_run.read_string
                  ) p lb
                )
              );
            | 2 ->
              field_lat := (
                Some (
                  (
                    Atdgen_runtime.Oj_run.read_number
                  ) p lb
                )
              );
            | 3 ->
              field_lon := (
                Some (
                  (
                    Atdgen_runtime.Oj_run.read_number
                  ) p lb
                )
              );
            | _ -> (
                Yojson.Safe.skip_json p lb
              )
        );
      done;
      assert false;
    with Yojson.End_of_object -> (
        (
          {
            country = (match !field_country with Some x -> x | None -> Atdgen_runtime.Oj_run.missing_field p "country");
            postal = (match !field_postal with Some x -> x | None -> Atdgen_runtime.Oj_run.missing_field p "postal");
            lat = (match !field_lat with Some x -> x | None -> Atdgen_runtime.Oj_run.missing_field p "lat");
            lon = (match !field_lon with Some x -> x | None -> Atdgen_runtime.Oj_run.missing_field p "lon");
          }
         : location)
      )
)
let location_of_string s =
  read_location (Yojson.Safe.init_lexer ()) (Lexing.from_string s)
let write__string_float_list = (
  Atdgen_runtime.Oj_run.write_list (
    fun ob x ->
      Buffer.add_char ob '(';
      (let x, _ = x in
      (
        Yojson.Safe.write_string
      ) ob x
      );
      Buffer.add_char ob ',';
      (let _, x = x in
      (
        Yojson.Safe.write_float
      ) ob x
      );
      Buffer.add_char ob ')';
  )
)
let string_of__string_float_list ?(len = 1024) x =
  let ob = Buffer.create len in
  write__string_float_list ob x;
  Buffer.contents ob
let read__string_float_list = (
  Atdgen_runtime.Oj_run.read_list (
    fun p lb ->
      Yojson.Safe.read_space p lb;
      let std_tuple = Yojson.Safe.start_any_tuple p lb in
      let len = ref 0 in
      let end_of_tuple = ref false in
      (try
        let x0 =
          let x =
            (
              Atdgen_runtime.Oj_run.read_string
            ) p lb
          in
          incr len;
          Yojson.Safe.read_space p lb;
          Yojson.Safe.read_tuple_sep2 p std_tuple lb;
          x
        in
        let x1 =
          let x =
            (
              Atdgen_runtime.Oj_run.read_number
            ) p lb
          in
          incr len;
          (try
            Yojson.Safe.read_space p lb;
            Yojson.Safe.read_tuple_sep2 p std_tuple lb;
          with Yojson.End_of_tuple -> end_of_tuple := true);
          x
        in
        if not !end_of_tuple then (
          try
            while true do
              Yojson.Safe.skip_json p lb;
              Yojson.Safe.read_space p lb;
              Yojson.Safe.read_tuple_sep2 p std_tuple lb;
            done
          with Yojson.End_of_tuple -> ()
        );
        (x0, x1)
      with Yojson.End_of_tuple ->
        Atdgen_runtime.Oj_run.missing_tuple_fields p !len [ 0; 1 ]);
  )
)
let _string_float_list_of_string s =
  read__string_float_list (Yojson.Safe.init_lexer ()) (Lexing.from_string s)
let write_package : _ -> package -> _ = (
  fun ob (x : package) ->
    Buffer.add_char ob '{';
    let is_first = ref true in
    if !is_first then
      is_first := false
    else
      Buffer.add_char ob ',';
      Buffer.add_string ob "\"db_nr\":";
    (
      Yojson.Safe.write_string
    )
      ob x.db_nr;
    if !is_first then
      is_first := false
    else
      Buffer.add_char ob ',';
      Buffer.add_string ob "\"customer_nr\":";
    (
      Yojson.Safe.write_int
    )
      ob x.customer_nr;
    if !is_first then
      is_first := false
    else
      Buffer.add_char ob ',';
      Buffer.add_string ob "\"articles\":";
    (
      write__string_float_list
    )
      ob x.articles;
    if !is_first then
      is_first := false
    else
      Buffer.add_char ob ',';
      Buffer.add_string ob "\"weight\":";
    (
      Yojson.Safe.write_float
    )
      ob x.weight;
    if !is_first then
      is_first := false
    else
      Buffer.add_char ob ',';
      Buffer.add_string ob "\"size\":";
    (
      Yojson.Safe.write_float
    )
      ob x.size;
    if !is_first then
      is_first := false
    else
      Buffer.add_char ob ',';
      Buffer.add_string ob "\"location\":";
    (
      write_location
    )
      ob x.location;
    if !is_first then
      is_first := false
    else
      Buffer.add_char ob ',';
      Buffer.add_string ob "\"deliverer\":";
    (
      Yojson.Safe.write_string
    )
      ob x.deliverer;
    if !is_first then
      is_first := false
    else
      Buffer.add_char ob ',';
      Buffer.add_string ob "\"is_damaged\":";
    (
      Yojson.Safe.write_bool
    )
      ob x.is_damaged;
    Buffer.add_char ob '}';
)
let string_of_package ?(len = 1024) x =
  let ob = Buffer.create len in
  write_package ob x;
  Buffer.contents ob
let read_package = (
  fun p lb ->
    Yojson.Safe.read_space p lb;
    Yojson.Safe.read_lcurl p lb;
    let field_db_nr = ref (None) in
    let field_customer_nr = ref (None) in
    let field_articles = ref (None) in
    let field_weight = ref (None) in
    let field_size = ref (None) in
    let field_location = ref (None) in
    let field_deliverer = ref (None) in
    let field_is_damaged = ref (None) in
    try
      Yojson.Safe.read_space p lb;
      Yojson.Safe.read_object_end lb;
      Yojson.Safe.read_space p lb;
      let f =
        fun s pos len ->
          if pos < 0 || len < 0 || pos + len > String.length s then
            invalid_arg (Printf.sprintf "out-of-bounds substring position or length: string = %S, requested position = %i, requested length = %i" s pos len);
          match len with
            | 4 -> (
                if String.unsafe_get s pos = 's' && String.unsafe_get s (pos+1) = 'i' && String.unsafe_get s (pos+2) = 'z' && String.unsafe_get s (pos+3) = 'e' then (
                  4
                )
                else (
                  -1
                )
              )
            | 5 -> (
                if String.unsafe_get s pos = 'd' && String.unsafe_get s (pos+1) = 'b' && String.unsafe_get s (pos+2) = '_' && String.unsafe_get s (pos+3) = 'n' && String.unsafe_get s (pos+4) = 'r' then (
                  0
                )
                else (
                  -1
                )
              )
            | 6 -> (
                if String.unsafe_get s pos = 'w' && String.unsafe_get s (pos+1) = 'e' && String.unsafe_get s (pos+2) = 'i' && String.unsafe_get s (pos+3) = 'g' && String.unsafe_get s (pos+4) = 'h' && String.unsafe_get s (pos+5) = 't' then (
                  3
                )
                else (
                  -1
                )
              )
            | 8 -> (
                match String.unsafe_get s pos with
                  | 'a' -> (
                      if String.unsafe_get s (pos+1) = 'r' && String.unsafe_get s (pos+2) = 't' && String.unsafe_get s (pos+3) = 'i' && String.unsafe_get s (pos+4) = 'c' && String.unsafe_get s (pos+5) = 'l' && String.unsafe_get s (pos+6) = 'e' && String.unsafe_get s (pos+7) = 's' then (
                        2
                      )
                      else (
                        -1
                      )
                    )
                  | 'l' -> (
                      if String.unsafe_get s (pos+1) = 'o' && String.unsafe_get s (pos+2) = 'c' && String.unsafe_get s (pos+3) = 'a' && String.unsafe_get s (pos+4) = 't' && String.unsafe_get s (pos+5) = 'i' && String.unsafe_get s (pos+6) = 'o' && String.unsafe_get s (pos+7) = 'n' then (
                        5
                      )
                      else (
                        -1
                      )
                    )
                  | _ -> (
                      -1
                    )
              )
            | 9 -> (
                if String.unsafe_get s pos = 'd' && String.unsafe_get s (pos+1) = 'e' && String.unsafe_get s (pos+2) = 'l' && String.unsafe_get s (pos+3) = 'i' && String.unsafe_get s (pos+4) = 'v' && String.unsafe_get s (pos+5) = 'e' && String.unsafe_get s (pos+6) = 'r' && String.unsafe_get s (pos+7) = 'e' && String.unsafe_get s (pos+8) = 'r' then (
                  6
                )
                else (
                  -1
                )
              )
            | 10 -> (
                if String.unsafe_get s pos = 'i' && String.unsafe_get s (pos+1) = 's' && String.unsafe_get s (pos+2) = '_' && String.unsafe_get s (pos+3) = 'd' && String.unsafe_get s (pos+4) = 'a' && String.unsafe_get s (pos+5) = 'm' && String.unsafe_get s (pos+6) = 'a' && String.unsafe_get s (pos+7) = 'g' && String.unsafe_get s (pos+8) = 'e' && String.unsafe_get s (pos+9) = 'd' then (
                  7
                )
                else (
                  -1
                )
              )
            | 11 -> (
                if String.unsafe_get s pos = 'c' && String.unsafe_get s (pos+1) = 'u' && String.unsafe_get s (pos+2) = 's' && String.unsafe_get s (pos+3) = 't' && String.unsafe_get s (pos+4) = 'o' && String.unsafe_get s (pos+5) = 'm' && String.unsafe_get s (pos+6) = 'e' && String.unsafe_get s (pos+7) = 'r' && String.unsafe_get s (pos+8) = '_' && String.unsafe_get s (pos+9) = 'n' && String.unsafe_get s (pos+10) = 'r' then (
                  1
                )
                else (
                  -1
                )
              )
            | _ -> (
                -1
              )
      in
      let i = Yojson.Safe.map_ident p f lb in
      Atdgen_runtime.Oj_run.read_until_field_value p lb;
      (
        match i with
          | 0 ->
            field_db_nr := (
              Some (
                (
                  Atdgen_runtime.Oj_run.read_string
                ) p lb
              )
            );
          | 1 ->
            field_customer_nr := (
              Some (
                (
                  Atdgen_runtime.Oj_run.read_int
                ) p lb
              )
            );
          | 2 ->
            field_articles := (
              Some (
                (
                  read__string_float_list
                ) p lb
              )
            );
          | 3 ->
            field_weight := (
              Some (
                (
                  Atdgen_runtime.Oj_run.read_number
                ) p lb
              )
            );
          | 4 ->
            field_size := (
              Some (
                (
                  Atdgen_runtime.Oj_run.read_number
                ) p lb
              )
            );
          | 5 ->
            field_location := (
              Some (
                (
                  read_location
                ) p lb
              )
            );
          | 6 ->
            field_deliverer := (
              Some (
                (
                  Atdgen_runtime.Oj_run.read_string
                ) p lb
              )
            );
          | 7 ->
            field_is_damaged := (
              Some (
                (
                  Atdgen_runtime.Oj_run.read_bool
                ) p lb
              )
            );
          | _ -> (
              Yojson.Safe.skip_json p lb
            )
      );
      while true do
        Yojson.Safe.read_space p lb;
        Yojson.Safe.read_object_sep p lb;
        Yojson.Safe.read_space p lb;
        let f =
          fun s pos len ->
            if pos < 0 || len < 0 || pos + len > String.length s then
              invalid_arg (Printf.sprintf "out-of-bounds substring position or length: string = %S, requested position = %i, requested length = %i" s pos len);
            match len with
              | 4 -> (
                  if String.unsafe_get s pos = 's' && String.unsafe_get s (pos+1) = 'i' && String.unsafe_get s (pos+2) = 'z' && String.unsafe_get s (pos+3) = 'e' then (
                    4
                  )
                  else (
                    -1
                  )
                )
              | 5 -> (
                  if String.unsafe_get s pos = 'd' && String.unsafe_get s (pos+1) = 'b' && String.unsafe_get s (pos+2) = '_' && String.unsafe_get s (pos+3) = 'n' && String.unsafe_get s (pos+4) = 'r' then (
                    0
                  )
                  else (
                    -1
                  )
                )
              | 6 -> (
                  if String.unsafe_get s pos = 'w' && String.unsafe_get s (pos+1) = 'e' && String.unsafe_get s (pos+2) = 'i' && String.unsafe_get s (pos+3) = 'g' && String.unsafe_get s (pos+4) = 'h' && String.unsafe_get s (pos+5) = 't' then (
                    3
                  )
                  else (
                    -1
                  )
                )
              | 8 -> (
                  match String.unsafe_get s pos with
                    | 'a' -> (
                        if String.unsafe_get s (pos+1) = 'r' && String.unsafe_get s (pos+2) = 't' && String.unsafe_get s (pos+3) = 'i' && String.unsafe_get s (pos+4) = 'c' && String.unsafe_get s (pos+5) = 'l' && String.unsafe_get s (pos+6) = 'e' && String.unsafe_get s (pos+7) = 's' then (
                          2
                        )
                        else (
                          -1
                        )
                      )
                    | 'l' -> (
                        if String.unsafe_get s (pos+1) = 'o' && String.unsafe_get s (pos+2) = 'c' && String.unsafe_get s (pos+3) = 'a' && String.unsafe_get s (pos+4) = 't' && String.unsafe_get s (pos+5) = 'i' && String.unsafe_get s (pos+6) = 'o' && String.unsafe_get s (pos+7) = 'n' then (
                          5
                        )
                        else (
                          -1
                        )
                      )
                    | _ -> (
                        -1
                      )
                )
              | 9 -> (
                  if String.unsafe_get s pos = 'd' && String.unsafe_get s (pos+1) = 'e' && String.unsafe_get s (pos+2) = 'l' && String.unsafe_get s (pos+3) = 'i' && String.unsafe_get s (pos+4) = 'v' && String.unsafe_get s (pos+5) = 'e' && String.unsafe_get s (pos+6) = 'r' && String.unsafe_get s (pos+7) = 'e' && String.unsafe_get s (pos+8) = 'r' then (
                    6
                  )
                  else (
                    -1
                  )
                )
              | 10 -> (
                  if String.unsafe_get s pos = 'i' && String.unsafe_get s (pos+1) = 's' && String.unsafe_get s (pos+2) = '_' && String.unsafe_get s (pos+3) = 'd' && String.unsafe_get s (pos+4) = 'a' && String.unsafe_get s (pos+5) = 'm' && String.unsafe_get s (pos+6) = 'a' && String.unsafe_get s (pos+7) = 'g' && String.unsafe_get s (pos+8) = 'e' && String.unsafe_get s (pos+9) = 'd' then (
                    7
                  )
                  else (
                    -1
                  )
                )
              | 11 -> (
                  if String.unsafe_get s pos = 'c' && String.unsafe_get s (pos+1) = 'u' && String.unsafe_get s (pos+2) = 's' && String.unsafe_get s (pos+3) = 't' && String.unsafe_get s (pos+4) = 'o' && String.unsafe_get s (pos+5) = 'm' && String.unsafe_get s (pos+6) = 'e' && String.unsafe_get s (pos+7) = 'r' && String.unsafe_get s (pos+8) = '_' && String.unsafe_get s (pos+9) = 'n' && String.unsafe_get s (pos+10) = 'r' then (
                    1
                  )
                  else (
                    -1
                  )
                )
              | _ -> (
                  -1
                )
        in
        let i = Yojson.Safe.map_ident p f lb in
        Atdgen_runtime.Oj_run.read_until_field_value p lb;
        (
          match i with
            | 0 ->
              field_db_nr := (
                Some (
                  (
                    Atdgen_runtime.Oj_run.read_string
                  ) p lb
                )
              );
            | 1 ->
              field_customer_nr := (
                Some (
                  (
                    Atdgen_runtime.Oj_run.read_int
                  ) p lb
                )
              );
            | 2 ->
              field_articles := (
                Some (
                  (
                    read__string_float_list
                  ) p lb
                )
              );
            | 3 ->
              field_weight := (
                Some (
                  (
                    Atdgen_runtime.Oj_run.read_number
                  ) p lb
                )
              );
            | 4 ->
              field_size := (
                Some (
                  (
                    Atdgen_runtime.Oj_run.read_number
                  ) p lb
                )
              );
            | 5 ->
              field_location := (
                Some (
                  (
                    read_location
                  ) p lb
                )
              );
            | 6 ->
              field_deliverer := (
                Some (
                  (
                    Atdgen_runtime.Oj_run.read_string
                  ) p lb
                )
              );
            | 7 ->
              field_is_damaged := (
                Some (
                  (
                    Atdgen_runtime.Oj_run.read_bool
                  ) p lb
                )
              );
            | _ -> (
                Yojson.Safe.skip_json p lb
              )
        );
      done;
      assert false;
    with Yojson.End_of_object -> (
        (
          {
            db_nr = (match !field_db_nr with Some x -> x | None -> Atdgen_runtime.Oj_run.missing_field p "db_nr");
            customer_nr = (match !field_customer_nr with Some x -> x | None -> Atdgen_runtime.Oj_run.missing_field p "customer_nr");
            articles = (match !field_articles with Some x -> x | None -> Atdgen_runtime.Oj_run.missing_field p "articles");
            weight = (match !field_weight with Some x -> x | None -> Atdgen_runtime.Oj_run.missing_field p "weight");
            size = (match !field_size with Some x -> x | None -> Atdgen_runtime.Oj_run.missing_field p "size");
            location = (match !field_location with Some x -> x | None -> Atdgen_runtime.Oj_run.missing_field p "location");
            deliverer = (match !field_deliverer with Some x -> x | None -> Atdgen_runtime.Oj_run.missing_field p "deliverer");
            is_damaged = (match !field_is_damaged with Some x -> x | None -> Atdgen_runtime.Oj_run.missing_field p "is_damaged");
          }
         : package)
      )
)
let package_of_string s =
  read_package (Yojson.Safe.init_lexer ()) (Lexing.from_string s)
