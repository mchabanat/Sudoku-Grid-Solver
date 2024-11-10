class DeductionRule:
    def __init__(self, solver):
        self.solver = solver  # Permet à chaque règle d'accéder aux méthodes du solver

    def apply(self, grid):
        raise NotImplementedError("Cette méthode doit être implémentée dans les sous classes")


class DR1(DeductionRule):
    """Règle de déduction 1 : Direct Solve."""
    def apply(self, grid):
        changed = False
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    possible_values = self.solver.possible_values(row, col)
                    if len(possible_values) == 1:
                        grid[row][col] = possible_values[0]
                        changed = True
                        print(f"DR1: Ajouté {possible_values[0]} à ({row}, {col})")
        return changed


class DR2(DeductionRule):
    """Règle de déduction 2 : Hidden Single."""
    def apply(self, grid):
        changed = False
        for num in range(1, 10):
            # Vérification par lignes
            for row in range(9):
                possible_positions = [
                    col for col in range(9)
                    if grid[row][col] == 0 and num in self.solver.possible_values(row, col)
                ]
                if len(possible_positions) == 1:
                    col = possible_positions[0]
                    grid[row][col] = num
                    print(f"DR2: Ajouté {num} à ({row}, {col}) par single caché dans la ligne")
                    changed = True

            # Vérification par colonnes
            for col in range(9):
                possible_positions = [
                    row for row in range(9)
                    if grid[row][col] == 0 and num in self.solver.possible_values(row, col)
                ]
                if len(possible_positions) == 1:
                    row = possible_positions[0]
                    grid[row][col] = num
                    print(f"DR2: Ajouté {num} à ({row}, {col}) par single caché dans la colonne")
                    changed = True

            # Vérification par blocs 3x3
            for box_row in range(0, 9, 3):
                for box_col in range(0, 9, 3):
                    possible_positions = [
                        (r, c) for r in range(box_row, box_row + 3) for c in range(box_col, box_col + 3)
                        if grid[r][c] == 0 and num in self.solver.possible_values(r, c)
                    ]
                    if len(possible_positions) == 1:
                        row, col = possible_positions[0]
                        grid[row][col] = num
                        print(f"DR2: Ajouté {num} à ({row}, {col}) par single caché dans le bloc")
                        changed = True

        return changed


class DR3(DeductionRule):
    """Règle de déduction 3 : Naked Pair."""
    def apply(self, grid):
        changed = False
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    possible_values = self.solver.possible_values(row, col)
                    if len(possible_values) == 2:
                        if self.naked_pair(grid, row, col, possible_values):
                            print(f"DR3: Naked Pair trouvé pour {possible_values} en ligne {row} ou colonne {col}")
                            changed = True
        return changed

    def naked_pair(self, grid, row, col, pair):
        """Vérifie et traite les paires nues dans la ligne ou colonne de la case (row, col)."""
        for idx in range(9):
            # Vérifier la ligne
            if grid[row][idx] == 0 and idx != col:
                other_possible = self.solver.possible_values(row, idx)
                if other_possible == pair:
                    if self.eliminate_from_others(grid, pair, row=row):
                        return True
            # Vérifier la colonne
            if grid[idx][col] == 0 and idx != row:
                other_possible = self.solver.possible_values(idx, col)
                if other_possible == pair:
                    if self.eliminate_from_others(grid, pair, col=col):
                        return True
        return False

    def eliminate_from_others(self, grid, pair, row=None, col=None):
        """Élimine les valeurs de `pair` des cases de la même ligne ou colonne sans les paires nues."""
        changed = False
        if row is not None:
            for j in range(9):
                if grid[row][j] == 0 and j not in [j for j in range(9) if self.solver.possible_values(row, j) == pair]:
                    possible_vals = self.solver.possible_values(row, j)
                    new_vals = [v for v in possible_vals if v not in pair]
                    if len(new_vals) == 1:
                        grid[row][j] = new_vals[0]
                        print(f"DR3: Éliminé dans ligne {row}, mis {new_vals[0]} à ({row}, {j})")
                        changed = True
        elif col is not None:
            for i in range(9):
                if grid[i][col] == 0 and i not in [i for i in range(9) if self.solver.possible_values(i, col) == pair]:
                    possible_vals = self.solver.possible_values(i, col)
                    new_vals = [v for v in possible_vals if v not in pair]
                    if len(new_vals) == 1:
                        grid[i][col] = new_vals[0]
                        print(f"DR3: Éliminé dans colonne {col}, mis {new_vals[0]} à ({i}, {col})")
                        changed = True
        return changed


class SudokuSolver:
    def __init__(self):
        self.rules = [DR1(self), DR2(self), DR3(self)]
        self.grid = [[0] * 9 for _ in range(9)]
        self.difficulty = "Inconnu"
        self.user_input_required = False

    def possible_values(self, row, col):
        values = set(range(1, 10))
        values -= set(self.grid[row])  
        values -= {self.grid[i][col] for i in range(9)}
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        values -= {self.grid[r][c] for r in range(box_row, box_row + 3) for c in range(box_col, box_col + 3)}
        return list(values)
    

    def load_grid_from_file(self, file_path):
        """Charge la grille depuis un fichier texte au format spécifié par l'utilisateur."""
        try:
            with open(file_path, 'r') as file:
                grid = []
                for line in file:
                    # Supprime les espaces, découpe la ligne par virgules et convertit en entiers
                    row = [int(num) for num in line.strip().split(',')]
                    if len(row) != 9:
                        raise ValueError("Chaque ligne doit contenir exactement 9 valeurs.")
                    grid.append(row)
                if len(grid) != 9:
                    raise ValueError("Le fichier doit contenir exactement 9 lignes.")
                self.grid = grid
                print("Grille chargée :")
                self.display_grid()
        except Exception as e:
            print(f"Erreur lors du chargement du fichier : {e}")
            raise

    def is_valid(self, row, col, value):
        """Vérifie si une valeur peut être placée dans une case sans violer les règles du Sudoku."""
        if value in self.grid[row]:
            return False
        if value in (self.grid[i][col] for i in range(9)):
            return False
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if self.grid[r][c] == value:
                    return False
        return True

    def prompt_user_for_value(self):
        """Demande à l'utilisateur de saisir une valeur pour une case vide et valide la saisie"""
        self.user_input_required = True  # Marque que l'intervention de l'utilisateur est nécessaire
        while True:
            try:
                # Demande et validation de la ligne
                row1 = self.get_integer_input("Entrez le numéro de ligne (0-8) : ", 0, 8)
                # Demande et validation de la colonne
                col1 = self.get_integer_input("Entrez le numéro de colonne (0-8) : ", 0, 8)
                
                # Vérifie si la case est vide avant d'entrer la valeur
                if self.grid[row1][col1] != 0:
                    print("Cette case est déjà remplie. Choisissez une case vide.")
                    continue

                # Demande et validation de la valeur
                value = self.get_integer_input(f"Entrez une valeur pour la case ({row1}, {col1}) (1-9) : ", 1, 9)
                
                # Vérification des règles de placement du Sudoku
                if self.is_valid(row1, col1, value):
                    self.grid[row1][col1] = value
                    print(f"Valeur {value} ajoutée en ({row1}, {col1})")
                    self.display_grid()  # Affiche la grille immédiatement après la saisie correcte
                    break  # Quitte la boucle car l'entrée est correcte
                else:
                    print("La valeur viole les contraintes du Sudoku. Essayez une autre valeur.")

            except ValueError:
                print("Entrée non valide.")

    def get_integer_input(self, prompt, min_value, max_value):
        """Demande à l'utilisteur de saisir un entier entre min_value et max_value inclus"""
        while True:
            try:
                value = int(input(prompt))
                if min_value <= value <= max_value:
                    return value
                else:
                    print(f"Entrée invalide. Veuillez entrer un nombre entre {min_value} et {max_value}.")
            except ValueError:
                print("Entrée non valide. Assurez-vous d'entrer un nombre entier.")

    def apply_rules(self):
        changed = True
        used_rules = set()  # Garde une trace des règles utilisées pour classifier la difficulté
        while changed:
            changed = False
            for rule in self.rules:
                if rule.apply(self.grid):
                    changed = True
                    used_rules.add(rule.__class__.__name__)
                    break
        self.classify_difficulty(used_rules)  # Classifie la difficulté une fois les règles appliquées

    def classify_difficulty(self, used_rules):
        """Classifie la difficulté en fonction des règles appliquées."""
        if "DR1" in used_rules and not {"DR2", "DR3"}.intersection(used_rules):
            self.difficulty = "Facile"
        elif "DR2" in used_rules and "DR3" not in used_rules:
            self.difficulty = "Moyen"
        elif "DR3" in used_rules and not self.user_input_required:
            self.difficulty = "Difficile"
        elif self.user_input_required:
            self.difficulty = "Très difficile"

    def solve(self):
        # Applique les règles pour résoudre autant de cases que possible
        self.apply_rules()
        # Continue à remplir les cases manuellement si les règles ne suffisent pas
        while any(0 in row for row in self.grid):  # Vérifie s'il reste des cases vides
            self.display_grid()
            print("Certaines cases sont encore vides. Les règles de déduction ne peuvent pas tout remplir.")
            self.prompt_user_for_value()  # Demande à l'utilisateur de remplir une case vide
            self.apply_rules()  # Réapplique les règles après chaque nouvelle valeur
        self.display_grid()
        print("Résolution complète !")

    def display_grid(self):
        for row in self.grid:
            print(" ".join(str(val) if val != 0 else "." for val in row))
        print()

# Fonction pour exécuter le solver avec affichage de la difficulté
def main():
    print("Veuillez entrer le chemin du fichier de la grille de Sudoku (format : chiffres séparés par des virgules, 0 pour les cases vides) :")
    file_path = input("Chemin du fichier : ")
    solver = SudokuSolver()
    try:
        solver.load_grid_from_file(file_path)
        solver.solve()
        print(f"Difficulté : {solver.difficulty}")
    except Exception as e:
        print("Une erreur est survenue :", e)

# Appel de la fonction principale pour démarrer l'application
if __name__ == "__main__":
    main()

