# Sudoku-Grid-Solver
Projet mi-semestre M1 Informatique - Software Engineering



## Guide d'exécution du solveur de Sudoku

#### 1. Exécuter le code
Pour exécuter le code, lancez le fichier Python contenant le solveur de Sudoku. Assurez-vous d'utiliser un environnement compatible avec Python 3.

#### 2. Ce que le code va faire
Le solveur de Sudoku est conçu pour résoudre une grille de Sudoku en appliquant nos trois règles de déduction. Le solveur procède par étapes :
- Il applique les règles de déduction dans l'ordre : **DR1 (Direct Solve)**, **DR2 (Hidden Single)**, et **DR3 (Naked Pair)**.
- Après avoir appliqué ces règles, il vérifie si toutes les cases sont remplies.
- Si toutes les cases sont remplies, la grille est considérée comme résolue.
- Si certaines cases restent vides et que les règles de déduction ne peuvent plus progresser, le solveur demandera à l’utilisateur d’intervenir.

#### 3. Fournir une grille de Sudoku au solveur
Pour fournir une grille à résoudre, vous devez créer un fichier texte contenant la grille. Ce fichier doit être au format suivant :
- Chaque ligne du fichier représente une ligne de la grille de Sudoku.
- Les chiffres d’une ligne sont séparés par des virgules, et chaque ligne doit contenir exactement 9 chiffres.
- Utilisez le chiffre `0` pour représenter une case vide.

**Exemple du format de grille attendue dans le fichier .txt** :
```
5,3,0,0,7,0,0,0,0
6,0,0,1,9,5,0,0,0
0,9,8,0,0,0,0,6,0
8,0,0,0,6,0,0,0,3
4,0,0,8,0,3,0,0,1
7,0,0,0,2,0,0,0,6
0,6,0,0,0,0,2,8,0
0,0,0,4,1,9,0,0,5
0,0,0,0,8,0,0,7,9
```

Lors de l'exécution, le programme demandera le chemin du fichier contenant la grille de Sudoku. Une fois que vous avez entré le chemin, si il est reconnue et que la grille est au bon format, le solveur se lance directement.

#### 4. Comportement du solveur et affichage des résultats
Le solveur suit une logique d'affichage selon le déroulement de la résolution :
En premier il affiche la grille initiale, puis à la suite il affiche pour toutes les valeurs remplies la règle de déduction qui à servi (DR1, DR2 ou DR3).
- **Si le solveur arrive à tout résoudre automatiquement** :
  - Il affichera la grille complète résolue.
  - Il indiquera également le niveau de difficulté estimé de la grille (Facile, Moyen, Difficile ou Très Difficile) en fonction des règles appliquées pour la résoudre.

- **Si le solveur atteint un blocage** (c'est-à-dire que les règles de déduction ne suffisent plus à résoudre toutes les cases) :
  - Le solveur affichera un message indiquant que certaines cases restent vides et que les règles de déduction ne peuvent pas remplir ces cases automatiquement.
  - La grille partiellement remplie sera affichée pour que l'utilisateur puisse visualiser l'état actuel.

#### 5. Interaction avec l’utilisateur en cas de blocage
Dans le cas où le solver bloque :

- **Saisie de la ligne et de la colonne** : Le solveur demandera à l'utilisateur d'entrer le numéro de la ligne (de 0 à 8) et le numéro de la colonne (de 0 à 8) où l'utilisateur souhaite remplir une valeur.
- **Saisie de la valeur** : L'utilisateur entre ensuite une valeur (de 1 à 9) pour cette case.
- **Validation** : Le solveur vérifiera si la valeur saisie respecte les règles du Sudoku (pas de doublons dans la ligne, la colonne ou le bloc 3x3). Si la valeur est valide, elle sera ajoutée à la grille ; sinon, l’utilisateur devra entrer une autre valeur. Il arrive que la valeur ne s’affiche pas directement après sa saisie, dans ce cas le solver va redemander 
Parfois la grille ne se met pas à jour directement après la saisie de la valeur, il va demander à nouveau un chiffre pour choisir la ligne de la prochaine valeur, il suffit de rentrer un chiffre puis la grille se mettra à jour. 
Après chaque saisie, le solveur tentera de réappliquer les règles de déduction pour progresser automatiquement autant que possible. Le processus se répète jusqu’à ce que la grille soit entièrement remplie.
Une fois la grille complétée, le solveur affichera la grille finale ainsi que le niveau de difficulté.
Lorsque l’utilisateur rempli certaines valeurs, il se peut que même si elle répondent aux contraintes du sudoku on se retrouve bloqué à la fin sans solution. Dans ce cas bien sur le solver ne pourra rien faire étant qu’il n’y a pas de backtracking.
