from typing import Optional
import os
import numpy as np
import lightgbm 
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, log_loss, recall_score
import argparse

DATASET_PATH = "../data/dataset_distance_and_location.jsonl"
TRAIN_PATH = "../data/synthetic/train_data.csv"
TEST_PATH = "../data/synthetic/test_data.csv"
SYNTHETIC_PATH = "../data/synthetic/synthetic_data_de.csv"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--learning-rate", type=float, default=0.1)
    parser.add_argument("--num-leaves", type=int, default=31)
    parser.add_argument("--max-depth", type=int, default=-1)
    parser.add_argument("--min-data-in-leaf", type=int, default=20)
    parser.add_argument("--num-boost-round", type=int, default=100)
    args = parser.parse_args()

    hyper_params = np.array([
        args.learning_rate, 
        args.num_leaves, 
        args.max_depth, 
        args.min_data_in_leaf, 
        args.num_boost_round
    ])

    dataset = Dataset()
    best_model = model_from_vector(hyper_params, dataset.x_train, dataset.y_train)
    y_pred = best_model.predict(dataset.x_test)
    y_true = dataset.y_test
    confusion = confusion_matrix(y_true, np.round(y_pred))
    print(confusion)
    acc = accuracy_score(y_true, np.round(y_pred))
    ll = log_loss(y_true, y_pred)
    recall = recall_score(y_true, np.round(y_pred))
    print(f"Best model: {acc}, {ll}, {recall}")


def singleton(cls):
    instances = {}

    def instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return instance

@singleton
class Dataset:
    def __init__(self):
        dataset = pd.read_json(DATASET_PATH, lines=True)
        x = dataset["vec_repr"].tolist()
        x = np.array(x)
        y = dataset["is_damaged"].to_numpy()

        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x, y, test_size=0.2, shuffle=True)

        # train_data = pd.read_csv(TRAIN_PATH, index_col=0)
        # test_data = pd.read_csv(TEST_PATH, index_col=0)
        # synthetic_data = pd.read_csv(SYNTHETIC_PATH, index_col=0)

        # train_data = pd.concat([train_data, synthetic_data])

        # train_data.sample(frac=1)
        # test_data.sample(frac=1)

        # self.x_train = train_data.loc[:, train_data.columns != "is_damaged"].values
        # self.y_train = train_data["is_damaged"].values

        # self.x_test = test_data.loc[:, test_data.columns != "is_damaged"].values
        # self.y_test = test_data["is_damaged"].values


def model_from_vector(
    input: np.ndarray, 
    x_train: np.ndarray, 
    y_train: np.ndarray,
) -> lightgbm.Booster:
    params = {
        "objective": "binary",
        "metric": "cross_entropy",
        "is_unbalance": True,
        "verbosity": -1,
        "learning_rate": input[0],
        "num_leaves": int(np.round(input[1])),
        "max_depth": int(np.round(input[2])),
        "min_data_in_leaf": int(np.round(input[3])),
    }

    train_data = lightgbm.Dataset(x_train, label=y_train)
    model = lightgbm.train(params, train_data, num_boost_round=int(np.round(input[4])))
    return model


def binary_cross_entropy(
    y_true: np.ndarray, 
    y_pred: np.ndarray, 
    is_unbalance: bool = True,
) -> float:
    epsilon = 1e-15
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)

    pos_weight = 1 if not is_unbalance else np.sum(y_true == 0) / np.sum(y_true == 1)
    loss = -np.mean(pos_weight * y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
    return loss

def lgbm_fitness(input: np.ndarray) -> float:
    dataset = Dataset()
    model = model_from_vector(input, dataset.x_train, dataset.y_train)
    y_pred = model.predict(dataset.x_test)
    score = binary_cross_entropy(dataset.y_test, y_pred)  
    return score



def differential_evolution(
    fitness_function: callable, 
    n: int,
    bounds: list[tuple[float, float]],
    cr: float = 0.9,
    f: float = 0.8,
    iterations: int = 50,
    mu: Optional[int] = None,
) -> np.ndarray:
    if not mu: 
        mu = 10 * n

    population = _initialize(mu, n, bounds)
    fitness = np.apply_along_axis(fitness_function, 1, population)

    for k in range(iterations):
        print(f"Iteration {k + 1}/{iterations}")
        for i in range(mu):
            indices = np.random.permutation(mu)[:3]
            x1, x2, x3 = population[indices]
            # best = population[np.argmin(fitness)]
            v = x1 + f * (x3 - x2)
            mask = np.random.rand(n) < cr
            new_individual = np.where(mask, v, population[i])
            new_individual = np.clip(new_individual, *zip(*bounds))
            new_fitness = fitness_function(new_individual)
            if new_fitness < fitness[i]:
                population[i] = new_individual
                fitness[i] = new_fitness

        intermediate_result = np.concatenate((population, fitness.reshape(-1, 1)), axis=1)
        intermediate_result = pd.DataFrame(intermediate_result, columns=["learning_rate", "num_leaves", "max_depth", "min_data_in_leaf", "num_boost_round", "fitness"])
        intermediate_result.sort_values("fitness", inplace=True)
        os.system("clear")
        print(intermediate_result.head(20))


    return population[np.argsort(fitness)]


def _initialize(
    mu: int,
    n: int, 
    bounds: list[tuple[float, float]],
) -> np.ndarray:
    if not mu:
        mu = 10 * n
    lower_bounds = np.array([lower for lower, _ in bounds])
    upper_bounds = np.array([upper for _, upper in bounds])
    init = np.random.uniform(lower_bounds, upper_bounds, (mu, n))

    return init


if __name__ == "__main__":
    main()
