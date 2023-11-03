#Modell zur Transportschadenvorhersage
##Vorgehen

1. 11/12 des Datensatzes wurden in einen Trainings- und Testdatensatz aufgeteilt. 
2. Das übrige 1/12 wird als Validierungsdatensatz herangezogen (enthält ausschließlich reale, keine synthetischen Daten)
3. Die *Minderheitsklasse* (_beschädigt_) wird mit Hilfe der Synthetic Minority Oversampling Technique oversampled.
4. Zur Klassifikation wird ein Random Forest Classifier benutzt.

##Datensatz

| Datensatz | Samples N | Samples T |
| - | - | - |
| Trainingsdatensatz | 71285 | 71265 | 
| Testdatensatz | 17829 | 17809 |
| Validierungs | 75 | 8100 |

##Ergebnisse
