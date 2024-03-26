## Evaluation verschiedener Modelle zur Vorhersage von Transportschäden

### Ordnerstruktur

Im Ordner `classifier` befinden sich Dateien zur Erstellung und Evaluation verschiedener Modelle zur 
Transportschadenvorhersage:
- *rf_classifier.py*: Datei für das Training und die Evaluation eines Random Forest Klassifizierers.
- *svc_classifier.py*: Datei für das Training und die Evaluation eines Support Vector Klassifizierers.
- *mixed_ensemble.py*: Datei für die Erstellung eines Ensemble Klassifizierers bestehend aus LightGBM und Support Vector Klassifizierern.
- *lgbm_only_ensemble.py*: Datei für die Erstellung eines Ensemble Klassifizierers bestehend aus LightGBM Klassifizierern.
- *grid_search_lgbm.py*: Implementierung einer GridSearch zur Hyperparameter-Optimierung eines LightGBM Modells.
- *gating.py*: Datei zur Erstellung eines Neuronalen Netzes, das für das Gating eines LGBM-Ensembles verantwortlich ist. Das Netz bestimmt für einen gegebenenen Datenpunkt, welche Klassifizierer es benutzen soll.

Im Ordner `geolocate` befinden sich Dateien zur Bestimmung des Längen- und Breitengrades einer Zielortes für eine 
Bestellung auf Grundlage der Postleitzahl. 

Darüber hinaus enthält der Ordner `map` eine html-Seite zur Visualisierung der Schadensraten pro Ort.

Der Ordner `preprocessor` umfasst eine Pipeline zur Aufbereitung und Bereinigung der rohen Excel-Dateien.

Der Ordner `vectorize` enthält ein Tool zur Vektorisierung eines Pakets inklusive der Distanzbestimmung von Espelkamp bis zum ermittelten Längen- und Breitengrad.

### Erläuterungen

Die Evaluation zur Beurteilung der Vorhersage von Transportschäden mit Hilfe von Methoden des
`Machine Learning` wird anhand verschiedener Konfigurationen durchgeführt. Dabei betreffen diese 
Konfiguration folgende Aspekte:

1. Beschaffenheit des Datensatzes (Vektorrepräsentation)
2. Aufteilung des Datensatzes in Test- und Trainings- sowie Validierungsdatensatz
3. Konfiguration der Methoden zur Berücksichtigung des Klassenungleichgewichts
4. Art des Modells zur Vorhersage
5. Konfiguration der Hyperparameter eines Modells

#### Beschaffenheit des Datensatzes 

In der folgendenen Evaluation werden zwei unterschiedliche Konfigurationen des Datensatzes betrachtet:
1. Der Datensatz beinhaltet keine Informationen bezüglich des Zielortes des Pakets. `(wol)`
2. Der Datensatz beinhaltet den Längen- und Breitengrad des Zielortes des Pakets. `(wl)`

#### Aufteilung des Datensatzes 

In der Evaluation wird ausschließlich das folgende Verfahren zur Aufteilung des Datensatzes in 
Trainings-, Test- und Validierungsdatensatz verwendet, dabei bleibt das Verhältnis zwischen 
*positive* und *negative* Samples in den Subdatensätzen erhalten:
1. 80% des ursprünglichen Datensatzes sind Teil des Trainingsdatensatzes. 
2. 80% des übrigen Datensatzes werden dem Testdatensatz zugewiesen.
3. Die übrigen 20% (4% vom ursprünglichen Datensatz) bilden den Validierungsdatensatz.

### Konfigurationen der Methoden zur Berücksichtigung des Klassenungleichgewichts

Es bestehen verschiedene Ansätze dem Klassenungleichgewicht des Datensatzes gerecht zu werden:
1. Random Under Sampling `(rus)`-> das zufällige Ziehen von Einträgen der Mehrheitsklasse bis die Anzahl der Einträge in der Minderheitsklasse erreicht ist.
2. Synthetic Over Sampling `(sos)` -> das Erzeugen neuer synthetischer Dateneinträge, bis die Anzahl der Einträge in der Mehrheitsklasse erreicht ist.
3. (Einführen eines Penalty Terms (Klassengewicht, `cw`) zur Verstärkung der Gewichtung eines Fehlers, wenn er in der Minderheitsklasse auftritt. Standardmäßig entspricht das Klassengewicht dem Verhältnis zwischen 
Mehrheits- und Minderheitsklasse. Dies ist Teil der Hyperparameter eines Modells)

Zusätzlich zu diesen Konfigurationen besteht die Möglichkeit zur weiterführenden Konfiguration unter
Angabe eines Verhältnisses. Das Verhältnis ist eins, wenn beide Klassen gleich groß sind.So kann bspw. solange die Methode des Random Under Samplings angewandt 
werden, bis ein zuvor vorgegebenes Verhältnis erreicht wird. Die Verwendung eines solchen Verhältnisses erlaubt es, verschiedene Verfahren zu kombinieren. Bspw. könnte ein Datensatz erst bis zu einem Verhältnis zwischen Mehrheits- und Minerheitsklasse von `0.2` undersampled werden und daraufhin die Minderheitsklasse oversampled.

In der Tabelle zur Evaluation werden die Verfahren mit ihrem Parameter zur Angabe des Verhältnisses und der Reihenfolge der Verwendung angegeben.

Bsp.:

`(rus0.2)->(sos1)`

### Art des Modells zur Vorhersage

Für die Klassifikation zweier Klassen eignen sich grunsätzlich verschiedene Verfahren. Im folgenden werden diese Verfahren betrachtet:
1. SVM (Support Vector Machine)
2. LightGBM (Effizientes Gradient Boosting Modell)

### Konfiguration der Hyperparameter eines Modells

Abhängig von der Art des Modells, erlauben diese unterschiedliche Konfigurationen von Hyperparametern.
Hier werden ausschließlich diese Parameter betrachtet (einschließlich der Klassengewichtung):

1. SVM Parameter:
    - Kernel `(K)`
    - Klassengewichtung `(cw)`
2. LightGBM Parameter:
    - Klassifizierungsthreshold `(th)`
    - Anzahl der Iterationen `(nbr)`
    - Klassengewichtung `(cw)`

### Evaluation der SVM Modelle

| Datensatz | Resampling | K | cw | TN | FP | FN | TP | Accuracy | Recall |
| - | - | - | - | - | - | - | - | - | - |
| wol | - | linear | 5:1 | 22273 | 0 | 206 | 0 | .991 | 0. | 
| wol | - | linear | 2000:1 | 1416 | 20860 | 1 | 202 | .072 | .995 |
| wol | - | linear | 10000:1 | 1729 | 20565 | 2 | 183 | .085 | .989 |
| wol | - | poly | 100:1 | 21109 | 1157 | 175 | 38 | .941 | .178 |
| wol | - | poly | 2000:1 | 1416 | 20860 | 1 | 202 | .072 | .995 |
| wol | - | poly | 10000:1 | 24 | 22249 | 0 | 206 | .01 | 1. |
| wol | - | poly | auto | 21165 | 1106 | 170 | 38 | .943 | .183 |
| wl | - | poly | auto | 16919 | 1440 | 144 | 38 | .915 | .21 |

### Evaluation der LightGBM Modelle

| Datensatz | Resampling | th | nbr | cw | TN | FP | FN | TP | Accuracy | Recall |
| - | - | - | - | - | - | - | - | - | - | - |
| wol | - | 0.6 | 1000 | auto | 21884 | 381 | 199 | 15 | .974 | .07 |
| wol | - | 0.4 | 1000 | auto | 21534 | 773 | 147 | 25 | .959 | .145 |
| wl | - | 0.4 | 1000 | auto | 18263 | 122 | 154 | 2 | .985 | .013 |
| wl | - | 0.3 | 500 | auto | 17663 | 724 | 136 | 18 | .954 | .117 |
| wl | - | 0.4 | 250 | auto | 16942 | 1430 | 131 | 38 | .916 | .225 |
| wol | - | 0.4 | 250 | auto | 15645 | 2181 | 106 | 51 | .873 | .325 |
| wol | (sos1) | 0.5 | 100 | auto | 17928 | 442 | 148 | 23 | .968 | .135 |
| wol | (sos1) | 0.3 | 500 | auto | 17993 | 379 | 152 | 17 | .971 | 0.1 |
| wol | (sos.5) -> (rus) | 0.5 | 100 | auto | 17842 | 528 | 146 | 25 | .964 | .146 |
| wol | (sos.1) -> (rus) | 0.5 | 100 | auto | 17370 | 1001 | 138 | 32 | .939 | .188 |

### Evaluation der Ensemble 

| TN | FP | FN | TP | Accuracy | Recall |
| - | - | - | - | - | - | 
| 13811 | 885 | 103 | 34 | .933 | .248 |


