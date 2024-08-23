import tkinter as tk
import random
import time
from collections import deque

class Labyrinthe:
    def __init__(self, largeur, hauteur, taille_cellule, complexity):
        self.largeur = largeur
        self.hauteur = hauteur
        self.taille_cellule = taille_cellule
        self.complexity = complexity
        self.matrice = self.creer_matrice()
        self.fenetre = tk.Tk()
        self.canvas = tk.Canvas(self.fenetre, width=largeur*taille_cellule, height=hauteur*taille_cellule)
        self.canvas.pack()
        self.couleurs = {}

    def creer_matrice(self):
        """Crée une matrice initiale avec des murs (-1) et des chemins (0)."""
        return [[-1 if i % 2 == 0 or j % 2 == 0 else 0 for j in range(self.largeur)] for i in range(self.hauteur)]

    def generer_couleur_pour_valeur(self, valeur):
        """Génère une couleur aléatoire basée sur une valeur donnée."""
        random.seed(valeur)
        return f'#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}'

    def get_couleur(self, valeur):
        """Retourne la couleur associée à une valeur, en la générant si nécessaire."""
        if valeur not in self.couleurs:
            self.couleurs[valeur] = self.generer_couleur_pour_valeur(valeur)
        return self.couleurs[valeur]

    def afficher_matrice(self):
        """Affiche la matrice avec des couleurs correspondant aux valeurs."""
        self.canvas.delete("all")
        for i in range(self.hauteur):
            for j in range(self.largeur):
                self.afficher_case(i, j)
        self.fenetre.update()

    def afficher_case(self, i, j):
        """Affiche une case de la matrice à la position (i, j)."""
        x0, y0 = j * self.taille_cellule, i * self.taille_cellule
        x1, y1 = x0 + self.taille_cellule, y0 + self.taille_cellule
        if self.matrice[i][j] == -1:
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="black")  # Murs en noir
        else:
            couleur = self.get_couleur(self.matrice[i][j])
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=couleur)
            self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=str(self.matrice[i][j]), fill="black")

    def ajouter_entree_sortie(self):
        """Ajoute l'entrée et la sortie du labyrinthe."""
        self.matrice[1][0] = 1  # Entrée
        self.matrice[self.hauteur - 2][self.largeur - 1] = 1  # Sortie

    def remplir_cases(self):
        """Remplit les cases accessibles de la matrice avec des valeurs uniques."""
        valeur = 1
        for i in range(1, self.hauteur, 2):
            for j in range(1, self.largeur, 2):
                self.matrice[i][j] = valeur
                valeur += 1
        self.afficher_matrice()

    def mettre_a_jour_region(self, ancienne_valeur, nouvelle_valeur):
        """Met à jour toutes les cellules ayant une ancienne valeur par une nouvelle valeur."""
        for x in range(self.hauteur):
            for y in range(self.largeur):
                if self.matrice[x][y] == ancienne_valeur:
                    self.matrice[x][y] = nouvelle_valeur

    def casser_mur(self):
        """Casse les murs pour créer un labyrinthe en connectant les régions."""
        murs = [(i, j) for i in range(1, self.hauteur-1, 2) for j in range(2, self.largeur-1, 2)] + \
               [(i, j) for i in range(2, self.hauteur-1, 2) for j in range(1, self.largeur-1, 2)]
        random.shuffle(murs)

        while True:
            has_changed = False
            for i, j in murs:
                if i % 2 == 1 and j % 2 == 0:  # Mur vertical
                    has_changed |= self.casser_mur_vertical(i, j)
                elif i % 2 == 0 and j % 2 == 1:  # Mur horizontal
                    has_changed |= self.casser_mur_horizontal(i, j)

            # Vérifier si toutes les cases ont la même valeur (une seule région connectée)
            valeurs = {self.matrice[x][y] for x in range(1, self.hauteur, 2) for y in range(1, self.largeur, 2)}
            if len(valeurs) == 1:
                break

    def casser_mur_vertical(self, i, j):
        """Casse un mur vertical si possible."""
        if self.matrice[i][j-1] != self.matrice[i][j+1]:
            nouvelle_valeur = min(self.matrice[i][j-1], self.matrice[i][j+1])
            ancienne_valeur = max(self.matrice[i][j-1], self.matrice[i][j+1])

            if nouvelle_valeur == 1 or ancienne_valeur == 1:
                nouvelle_valeur = 1

            self.mettre_a_jour_region(ancienne_valeur, nouvelle_valeur)
            self.matrice[i][j] = nouvelle_valeur
            self.afficher_matrice()
            time.sleep(0.01)
            return True
        return False

    def casser_mur_horizontal(self, i, j):
        """Casse un mur horizontal si possible."""
        if self.matrice[i-1][j] != self.matrice[i+1][j]:
            nouvelle_valeur = min(self.matrice[i-1][j], self.matrice[i+1][j])
            ancienne_valeur = max(self.matrice[i-1][j], self.matrice[i+1][j])

            if nouvelle_valeur == 1 or ancienne_valeur == 1:
                nouvelle_valeur = 1

            self.mettre_a_jour_region(ancienne_valeur, nouvelle_valeur)
            self.matrice[i][j] = nouvelle_valeur
            self.afficher_matrice()
            time.sleep(0.01)
            return True
        return False

    def transformer_chemins(self):
        """Transforme toutes les cases ayant la valeur 1 en chemins (0)."""
        for i in range(self.hauteur):
            for j in range(self.largeur):
                if self.matrice[i][j] == 1:
                    self.matrice[i][j] = 0

    def afficher_matrice_2(self):
        """Affiche la matrice avec un dégradé de couleurs pour les valeurs."""
        self.canvas.delete("all")
        valeurs_positives = [cell for row in self.matrice for cell in row if cell > 0]

        if valeurs_positives:
            max_value = max(valeurs_positives)
            min_value = min(valeurs_positives)
        else:
            max_value = min_value = 1

        for i in range(self.hauteur):
            for j in range(self.largeur):
                self.afficher_case_degrade(i, j, min_value, max_value)
        self.fenetre.update()

    def afficher_case_degrade(self, i, j, min_value, max_value):
        """Affiche une case avec un dégradé de couleur basé sur la valeur."""
        x0, y0 = j * self.taille_cellule, i * self.taille_cellule
        x1, y1 = x0 + self.taille_cellule, y0 + self.taille_cellule
        if self.matrice[i][j] == -1:
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="black")  # Murs en noir
        elif self.matrice[i][j] == 0:
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="white")  # Chemin en blanc
        else:
            couleur = self.get_couleur_degrade(self.matrice[i][j], min_value, max_value)
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=couleur)  # Autres cases

    def generer_couleur_degrade(self, valeur, min_value, max_value):
        """Génère un dégradé de couleur du rouge au bleu basé sur une valeur relative entre min_value et max_value."""
        if max_value == min_value:
            return "#ffff00"  # Jaune si toutes les valeurs sont identiques
        ratio = (valeur - min_value) / (max_value - min_value)
        r = int(255 * (1 - ratio))
        g = int(255 * (1 - ratio) * 0.5)
        b = int(255 * ratio)
        return f'#{r:02x}{g:02x}{b:02x}'

    def get_couleur_degrade(self, valeur, min_value, max_value):
        """Retourne une couleur dégradée pour une valeur donnée."""
        return self.generer_couleur_degrade(valeur, min_value, max_value)

    def resolveuse(self):
        """Résout le labyrinthe en utilisant une approche de type BFS."""
        file = deque([(self.hauteur - 2, self.largeur - 1)])
        self.matrice[self.hauteur - 2][self.largeur - 1] = 1
        self.afficher_matrice_2()
        time.sleep(0.1)

        while file:
            x, y = file.popleft()
            valeur_actuelle = self.matrice[x][y]

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.hauteur and 0 <= ny < self.largeur and self.matrice[nx][ny] == 0:
                    self.matrice[nx][ny] = valeur_actuelle + 1
                    file.append((nx, ny))
                    self.afficher_matrice_2()
                    time.sleep(0.1)

            if (x, y) == (1, 0):
                break

    def rendre_complexe(self, nombre_murs):
        """Ajoute des murs supplémentaires pour complexifier le labyrinthe."""
        for _ in range(nombre_murs):
            i, j = random.choice([(i, j) for i in range(1, self.hauteur-1) for j in range(1, self.largeur-1) if self.matrice[i][j] == -1])
            self.matrice[i][j] = 1
            self.afficher_matrice()
            time.sleep(0.1)

    def marquer_solution(self):
        """Marque la solution du labyrinthe en vert."""
        x, y = 1, 0
        valeur_actuelle = self.matrice[x][y]

        while valeur_actuelle > 1:
            self.marquer_case(x, y, "green")
            time.sleep(0.1)

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.hauteur and 0 <= ny < self.largeur and self.matrice[nx][ny] == valeur_actuelle - 1:
                    x, y = nx, ny
                    valeur_actuelle -= 1
                    break

        self.marquer_case(x, y, "green")

    def marquer_case(self, x, y, couleur):
        """Colorie une case en (x, y) avec la couleur spécifiée."""
        self.canvas.create_rectangle(y * self.taille_cellule, x * self.taille_cellule,
                                     (y + 1) * self.taille_cellule, (x + 1) * self.taille_cellule,
                                     fill=couleur)
        self.fenetre.update()

    def generer_labyrinthe(self):
        """Génère le labyrinthe complet et le résout."""
        self.remplir_cases()
        self.ajouter_entree_sortie()
        time.sleep(1)
        self.casser_mur()
        self.rendre_complexe(self.complexity)
        self.transformer_chemins()
        self.afficher_matrice_2()
        self.resolveuse()
        self.marquer_solution()
        self.fenetre.mainloop()

# Créer et lancer le labyrinthe
labyrinthe = Labyrinthe(21, 20, 20, 9)
labyrinthe.generer_labyrinthe()
