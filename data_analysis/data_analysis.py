import seaborn as sns
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

def main():
    df = pd.read_csv("../data/packaging_lab_dataset_locations.csv", index_col=0)



    # plt.violinplot(df[df["is_damaged"] == 1]["weight"])
    # # make it such that the y axis goes to df["weight"] max
    # plt.ylim(0, df["weight"].max())
    # plt.savefig("./plots/damaged_weight_violin.png")
    # plt.clf()

    # plt.violinplot(df[df["is_damaged"] == 1]["size"])
    # plt.ylim(0, df["size"].max())
    # plt.savefig("./plots/damaged_size_violin.png")
    # plt.clf()
    # print(df.iloc[:, :5].describe())
    # sns.scatterplot(data=df, x="latitude", y="longitude", hue="is_damaged", alpha=0.2)

    # sns.scatterplot(data=df, x="distance", y="weight", hue="is_damaged")

    # plt.show()

    # all_deliverer_frequencies = df.iloc[:, 32:32+16].sum(axis=0)
    # all_article_frequencies = df.iloc[:, 32+16:].sum(axis=0)


    # damaged_deliverer_frequencies = df[df["is_damaged"] == 1].iloc[:, 32:32+16].sum(axis=0) 
    # damaged_article_frequencies = df[df["is_damaged"] == 1].iloc[:, 32+16:].sum(axis=0) 



    # plt.bar(deliverer_frequencies.index, deliverer_frequencies.values)
    # plt.xticks(rotation=90)
    # plt.show()

    # plt.bar(all_article_frequencies.index, all_article_frequencies.values)
    # plt.bar(damaged_article_frequencies.index, damaged_article_frequencies.values)
    # plt.xticks(rotation=90)
    # plt.show()


    # plt.show()

    # for column in df.columns:
    #     print(column)
    #     df[column].plot.hist()
    #     df[df["is_damaged"] == 1][column].plot.hist()
    #     plt.savefig(f"./plots/{column}.png")
    #     plt.clf()

    # for i in df.columns:
    #     for j in df.columns:
    #         print(i, j)
    #         sns.scatterplot(data=df, x=i, y=j, hue="is_damaged")
    #         plt.savefig(f"./plots/{i}_{j}.png")
    #         plt.clf()

    # q_25, q_50, q_75 = np.percentile(df["weight"], [25, 50, 75])
    # print(q_25, q_50, q_75)
    # print(df.loc[df["weight"] < q_25, "weight"])
    # print(df.loc[df["weight"] > q_75, "weight"])

    print(df["size"].describe())

    article_columns = df.iloc[:, 34+16:df.shape[1]-1]
    print(article_columns.columns)
    # undo one-hot encoding
    article_columns = article_columns.idxmax(axis=1)
    weight_column = df[["weight", "size"]]
    all = pd.concat([article_columns, weight_column], axis=1)
    all = all.sort_values(by="weight")
    all.to_csv("./weight_with_article.csv")

    # df["weight"].plot.box()
    # plt.savefig("./plots/weight_boxplot.png")
    # plt.clf()

    # df["size"].plot.box()
    # plt.savefig("./plots/size_boxplot.png")
    # plt.clf()


    # damaged_size = df[df["is_damaged"] == 1]["size"]
    # size = df["size"]
    # # make the histograms slightly transparent
    # plt.hist(size, density=True, alpha=.5)
    # plt.hist(damaged_size, density=True, alpha=.5)

    # plt.savefig("./plots/size.png")
    # plt.clf()

    # damaged_weight = df[df["is_damaged"] == 1]["weight"]
    # weight = df["weight"]
    # plt.hist(weight, density=True, alpha=.5)
    # plt.hist(damaged_weight, density=True, alpha=.5)
    # plt.savefig("./plots/weight.png")
    # plt.clf()


    # sns.scatterplot(data=df, x="size", y="weight", hue="is_damaged", alpha=0.5)
    # plt.savefig("./plots/size_weight.png")
    # plt.clf()

    # sns.scatterplot(data=df[df["is_damaged"] == 1], x="size", y="weight")
    # plt.savefig("./plots/size_weight_damaged.png")
    # plt.clf()
    # sns.scatterplot(data=df[df["is_damaged"] == 0], x="size", y="weight")
    # plt.savefig("./plots/size_weight_not_damaged.png")
    # plt.clf()
    

    # scalable_columns = df[["weight", "size", "distance", "latitude", "longitude"]]
    # scaler = StandardScaler()
    # x_std = scaler.fit_transform(scalable_columns)
    # df[["weight", "size", "distance", "latitude", "longitude"]] = x_std

    # x = df.loc[:, df.columns != "is_damaged"].values
    # tsne = TSNE(n_components=2, perplexity=15, learning_rate=10)
    # x_embedded = tsne.fit_transform(x)
    # embedded_df = pd.DataFrame(x_embedded)
    # embedded_df["is_damaged"] = df["is_damaged"]
    # sns.scatterplot(data=embedded_df, x=0, y=1, hue="is_damaged", alpha=0.2)
    # plt.savefig("./plots/tsne.png")

    
if __name__ == "__main__":
    main()

