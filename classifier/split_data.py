import pandas as pd
from sklearn.model_selection import train_test_split

def main():
    dataset = pd.read_json("../data/dataset_distance_and_location.jsonl", lines=True)
    y = dataset["is_damaged"].values
    x = dataset.drop(["is_damaged"], axis=1).values
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

    train = pd.DataFrame(x_train, columns=dataset.columns[:-1])
    train["is_damaged"] = y_train
    train.to_csv("../data/train.csv", index=False)

    test = pd.DataFrame(x_test, columns=dataset.columns[:-1])
    test["is_damaged"] = y_test
    test.to_csv("../data/test.csv", index=False)

if __name__ == "__main__":
    main()
