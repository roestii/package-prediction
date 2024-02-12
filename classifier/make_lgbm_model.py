import lightgbm
import numpy as np
import pandas as pd
import argparse
from sklearn.metrics import accuracy_score, recall_score
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--learning-rate', type=float, required=True)
    parser.add_argument('--max-depth', type=int, required=True)
    parser.add_argument('--num-leaves', type=int, required=True)
    parser.add_argument('--min-data-in-leaf', type=int, required=True)
    parser.add_argument('--num-boost-round', type=int, required=True)
    parser.add_argument('--train-data', type=str, required=True)
    parser.add_argument('--test-data', type=str, required=True)

    args = parser.parse_args()

    train_data = pd.read_csv(args.train_data)
    y_train = train_data["is_damaged"].values
    x_train = train_data["vec_repr"]
    x_train = x_train.apply(lambda x: json.loads(x))
    x_train = np.array(x_train.tolist())

    test_data = pd.read_csv(args.test_data)
    y_test = test_data["is_damaged"].values
    x_test = test_data["vec_repr"]
    x_test = x_test.apply(lambda x: json.loads(x))
    x_test = np.array(x_test.tolist())

    dataset = lightgbm.Dataset(x_train, label=y_train)

    params = {
        "is_unbalance": True,
        "objective": "binary",
        "learning_rate": args.learning_rate,
        "max_depth": args.max_depth,
        "num_leaves": args.num_leaves,
        "min_data_in_leaf": args.min_data_in_leaf,
    }

    model = lightgbm.train(params, dataset, args.num_boost_round)

    y_pred = np.array([model.predict([x])[0] for x in x_test])
    acc = accuracy_score(y_test, np.round(y_pred))
    recall = recall_score(y_test, np.round(y_pred))
    print(f"Acc: {acc}, Recall: {recall}")

    model.save_model("./models/model.pkl")


if __name__ == "__main__":
    main()
