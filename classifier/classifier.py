from imblearn.over_sampling import SMOTE
import pickle
from imblearn.under_sampling import ClusterCentroids, RandomUnderSampler
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import json
import numpy

def feature_names():
    return [
        "weight",
        "size",
        "AT",
        "AU",
        "BE",
        "BG",
        "BH",
        "CA",
        "CH",
        "CZ",
        "DE",
        "DK",
        "EE",
        "ES",
        "FR",
        "GE",
        "GR",
        "HR",
        "HU",
        "IE",
        "IT",
        "LI",
        "LU",
        "MG",
        "MT",
        "NL",
        "NZ",
        "PT",
        "RO",
        "RS",
        "SE",
        "SI",
        "Abholer",
        "Abholung",
        "Auslfa",
        "Dhl",
        "Infehler",
        "Kep",
        "Meyerjumb",
        "Post",
        "Sped",
        "Speddsv",
        "Sped_osna",
        "Tour_sped",
        "Ups",
        "Ups_a_geb",
        "Ups_ch",
        "Werkvk",
        "Abschluss",
        "Anleitung",
        "Bediensch",
        "Befestigun",
        "Buersten",
        "Dichtungen",
        "Endkappen",
        "Etiketten",
        "Faltrollo",
        "Federn",
        "Fvorhang",
        "Fuehrungspr",
        "Getriebe",
        "Holzprof",
        "Inschutz",
        "Jalousie",
        "Kartons",
        "Keder",
        "Ketten",
        "Klebebaende",
        "Klett",
        "Kollektion",
        "Kopfprof",
        "Kordeln",
        "Lacke",
        "Lamelle",
        "Lamellenvo",
        "Leihmesses",
        "Massiv",
        "Motoren",
        "Muttern",
        "Papprohe",
        "Plissee_20",
        "Plissee_wa",
        "Pospraes",
        "Ppshop",
        "Produktbau",
        "Produktion",
        "Prospekte",
        "Praesenter",
        "Pruefung",
        "Reparatur",
        "Rollen",
        "Rollo",
        "Rollwagen",
        "Rundrohr",
        "Scheiben",
        "Schnur",
        "Schrauben",
        "Schreibwar",
        "Shutters",
        "Sonderanfe",
        "Sonstige",
        "Stifte",
        "Variorollo",
        "Verpackung",
        "Vorhaenge",
        "Werbemitte",
        "Zubehoer",
        "Zubehoerbeu",
    ]

#assuming the given file has the jsonl format
def dataset_from_path(path, ratio=0.5):
    with open(path, "r") as dataset_file:
        entries = list(map(json.loads, dataset_file))
        xs = list(map(lambda x: x["vec_repr"], entries))
        ys = list(map(lambda x: x["is_damaged"], entries))
        return (numpy.array(xs), numpy.array(ys))
            
class RfClassifier:
    def __init__(
        self, 
        dataset, 
        classifier=RandomForestClassifier(), 
        undersampler=RandomUnderSampler(), 
        oversampler=SMOTE(),
        ratio=.2
    ):
        self.dataset = dataset
        self.classifier = classifier
        self.undersampler = undersampler
        self.ratio = ratio
        self.oversampler = oversampler

    def oversample(self):
        x, y = self.dataset
        self.dataset = self.oversampler.fit_resample(x, y)

    def undersample(self):
        x, y = self.dataset
        self.dataset = self.undersampler.fit_resample(x, y)
        print(self.dataset[0][0])

    def fit(self) :
        x, y = self.dataset
        x_train, x_test, y_train, y_test = train_test_split(x, y, shuffle=True, test_size=self.ratio)

        train_positives = list(filter(lambda x: x == 1, y_train))
        train_negatives = list(filter(lambda x: x == 0, y_train))
        print("len train :", len(y_train))
        print("train positives: ", len(train_positives))
        print("train negatives: ", len(train_negatives))
        print("train ratio: ", len(train_positives) / len(y_train))

        test_positives = list(filter(lambda x: x == 1, y_test))
        test_negatives = list(filter(lambda x: x == 0, y_test))
        print("len test: ", len(y_test))
        print("test positives: ", len(test_positives))
        print("test positives: ", len(test_negatives))
        print("test: ", len(test_positives) / len(y_test))

        self.classifier.fit(x_train, y_train)
        y_pred = self.classifier.predict(x_test)
        accuracy = accuracy_score(y_test, y_pred)
        cf_matrix = confusion_matrix(y_test, y_pred)
        print(accuracy)
        print(cf_matrix)

    def visualize(self):
        plt.figure(figsize=(10, 6))
        plot_tree(self.classifier.estimators_[0], filled=True, feature_names=feature_names(), class_names=["damaged", "not damaged"])
        plt.show()

    def save(self, path):
        with open(path, "wb") as out:
            pickle.dump(self, out)

def main():
    dataset = dataset_from_path("../data/dataset_base.jsonl")
    model = RfClassifier(dataset)
    #model.undersample()
    model.oversample()
    model.fit()
    model.save("oversampled.pkl")
    #model.visualize()
    #model.save("cs_undersampled.pkl")
    #_, y = model.dataset

    #positives = list(filter(lambda x: x == 1, y))
    #negatives = list(filter(lambda x: x == 0, y))

    #print("positives: ", len(positives))
    #print("negatives: ", len(negatives))
    

if __name__ == "__main__":
    main()
