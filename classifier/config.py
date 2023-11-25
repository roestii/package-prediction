from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

svm_configs = [
    {
        "name": "poly_wl_cwbalanced",
        "includes_locations": True,
        "class_weight": "balanced",
        "kernel": "poly",
    },
    {
        "name": "linear_wol_cwbalanced",
        "includes_locations": False,
        "class_weight": "balanced",
        "kernel": "linear",
    },
    {
        "name": "poly_wol_cwbalanced_smote03",
        "includes_locations": False,
        "class_weight": "balanced",
        "kernel": "poly",
        "over_sampler": SMOTE(random_state=42, sampling_strategy=0.3)
    },
]

lgbm_configs = [
    {
        "name": "lgbm_wl_smote01_rus_t05_n100",
        "includes_locations": True,
        "params": {
            "objective": "binary",
            "metric": "binary_logloss",
        },
        "over_sampler": SMOTE(random_state=42, sampling_strategy=0.1),
        "under_sampler": RandomUnderSampler(random_state=42),
        "threshold": 0.5,
        "num_boost_round": 100
    },
    {
        "name": "lgbm_wol_t04_n250",
        "includes_locations": False,
        "params": {
            "objective": "binary",
            "metric": "binary_logloss",
            "is_unbalance": True,
        },
        "threshold": 0.4,
        "num_boost_round": 250 
    },
    {
        "name": "lgbm_wl_t04_n250",
        "includes_locations": True,
        "params": {
            "objective": "binary",
            "metric": "binary_logloss",
            "is_unbalance": True,
        },
        "threshold": 0.4,
        "num_boost_round": 250 
    },
    {
        "name": "lgbm_wl_t03_n500",
        "includes_locations": True,
        "params": {
            "objective": "binary",
            "metric": "binary_logloss",
            "is_unbalance": True,
        },
        "threshold": 0.3,
        "num_boost_round": 500 
    },
]
