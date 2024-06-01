import pandas as pd

def main():
    df = pd.read_csv("../data/grid_search_results.csv")
    df["sorter"] = (df["test_recall"] + df["test_accuracy"]) / 2
    df = df.sort_values(by="sorter", ascending=False)
    df = df.loc[:20,:]
    df.to_csv("../data/grid_search_results_top.csv", index=False)


if __name__ == "__main__":
    main()
