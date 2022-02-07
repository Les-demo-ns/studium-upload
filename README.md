# studium-upload
Uploads to Studium

1. Go on studium, go in gradebook, select "Notes > Exporter > Fichier texte", download. In this example we saved it as "studium.csv".
2. Make a csv for the grades you want to upload. Must be of shape [matricule, grade1, grade2, ...]. **No csv header.** In this example, we saved it as "grades.csv".
3. Run this script:
  ```bash
  python3 main.py studium.csv grades.csv "TP0 (Brut)" TP1 Exam1
```
  or

  ```bash
  python3 main.py studium.csv grades.csv "TP0 (Brut)"
```
  etc. Obviously, you must give the column names so that their order corresponds to the order in your grading CSV.
  For example, if in my grading CSV it goes "matricule, grade for tp0, grade for exam1", I'd write 
  ```bash
  python3 main.py studium.csv grades.csv "TP0 (Brut)" Exam1
```
  , or whatever the corresponding names on studium are.
4. Script will merge the studium CSV and your grading CSV. It will output it as "results.csv". It will also output a "notfound.csv" containing all the matricules from the studium CSV that weren't matched.
5. Go on studium, go in gradebook, selection "Notes > Importation > Fichier CSV", import your "results.csv" (you must be a "Enseignant associé" on studium to see the "Importation" tab).
6. All 5 steps above must be ran everytime you update the grades, because if someone else edits the grades on studium, studium will complain if you try to use the old "studium.csv" in the import.
7. Send a blood sacrifice to Charlie so that their eldritch glory might grow. Thanks.
