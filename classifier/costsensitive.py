import pandas as pd
from sklearn import svm
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

def main():
    dataset_path = "../data/dataset_with_locations.jsonl"
    #validation_path = "../data/with_cutted/cutted.jsonl"

    (x, y) = dataset(dataset_path)
    #(x_val, y_val) = dataset(validation_path)
    (x_train, x_test, y_train, y_test) = train_test_split(x, y, shuffle=True, test_size=0.2)
    (x_train, x_val, y_train, y_val) = train_test_split(x_train, y_train, shuffle=True, test_size=0.2)

    #weights = {
    #    0: 1,
    #    1: 100,
    #}

    #Default kernel is linear
    #A poly kernel does significantly increase the time needed to compute a solution
    #setting the `class_weight` parameter to `balanced` such that the implementation uses
    #the builtin mechanism to determine the class weights
    classifier = svm.SVC(class_weight="balanced", kernel="poly")
    classifier.fit(x_train, y_train)

    #Testing the accuracy based on the test dataset, which might contain synthetic data 
    y_pred = classifier.predict(x_test)
    accuracy = accuracy_score(y_true=y_test, y_pred=y_pred)
    matrix = confusion_matrix(y_true=y_test, y_pred=y_pred)
    print(accuracy)
    print(matrix)

    #Testing the accuracy based on the validation dataset, which represents real world data
    y_pred = classifier.predict(x_val)
    accuracy = accuracy_score(y_true=y_val, y_pred=y_pred)
    matrix = confusion_matrix(y_true=y_val, y_pred=y_pred)
    print(accuracy)
    print(matrix)

def dataset(path: str) -> tuple[list[float], list[float]]:
    with open(path, "r") as file:
        df = pd.read_json(file, lines=True)
        x = df["vec_repr"].to_list()
        y = df["is_damaged"].to_list()
        return (x, y)


if __name__ == "__main__":
    main()
