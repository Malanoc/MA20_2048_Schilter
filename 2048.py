# ================================================================================================================================
# Projet: 2048- MA-20 - 2026
# Auteur: Marc Schilter - SI-CA1a
# Description: Ce projet est une implémentation du jeu 2048 en Python.
# Le but du jeu est de faire glisser les tuiles sur une grille pour combiner les tuiles de même valeur et atteindre la tuile 2048.
# ================================================================================================================================
from tkinter import messagebox
import tkinter as tk
import DisplayParam as dp
import random

# =========================================================
# 1. Création de la fenêtre principale
# =========================================================

window = tk.Tk()
window.title("2048")
window.geometry("1168x990")
window.resizable(False, False)
window.configure(bg=dp.BACKGROUND_COLOR_GAME)

# =========================================================
# 2. Interface haut de l'écran
# =========================================================

label_title = tk.Label(
    window,
    text="2048",
    font=("Arial", 48, "bold"),
    bg=dp.BACKGROUND_COLOR_GAME
)
label_title.place(x=330, y=105)

label_rule= tk.Label(
    window,
    text="Glissez les chiffres et obtenez la tuile 2048 !",
    font= ("Arial", 16, "bold"),
    bg=dp.BACKGROUND_COLOR_GAME
)
label_rule.place(x=330, y=190)

label_score_title = tk.Label(
    window,
    text="Score",
    font=("Arial", 16, "bold"),
    bg=dp.BACKGROUND_COLOR_GRID,
    width=6,
    height=2,
)
label_score_title.place(x=740, y=105)

score=0

label_score = tk.Label(
    window,
    text=str(score),
    font=("Arial", 16, "bold"),
    bg=dp.BACKGROUND_COLOR_GRID,
    width=6
)
label_score.place(x=740, y=145)

label_top_title = tk.Label(
    window,
    text="Top",
    font=("Arial", 16, "bold"),
    bg=dp.BACKGROUND_COLOR_GRID,
    width=6,
    height=2,
)
label_top_title.place(x=840, y=105)

top =0

label_top = tk.Label(
    window,
    text=str(top),
    font=("Arial", 16, "bold"),
    bg=dp.BACKGROUND_COLOR_GRID,
    width=6
)
label_top.place(x=840, y=145)

won = False
def new_game():
    global game, score, moves
    #réinitialise le score à 0 et met à jour l'affichage du score
    score = 0
    label_score.config(text=str(score))
    #vérifie le top score dans top_score.txt et le charge dans la variable top pour l'afficher
    global top
    try:
        with open("top_score.txt", "r") as file:
            top = int(file.read())
    except FileNotFoundError:
        top = 0
    label_top.config(text=str(top))

    #Génère une nouvelle grille de jeu avec des tuiles vides (0) et place deux tuiles de départ (2 ou 4) dans des cases aléatoires.
    #la fonction new_game appelle une fonction tile_generator qui génère une nouvelle tuile dans une case vide de la grille.
    game = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    moves = 1   #moves est mis à 1 pour que la fonction tile_generator puisse générer une tuile au début du jeu
    tile_generator()
    tile_generator()
    update_grid()


btn_new = tk.Button(
    window,
    text="Nouveau",
    command=new_game,
    bg=dp.BACKGROUND_COLOR_GAME,
    width=12,
    height=2,
)
btn_new.place(x=830, y=190)

# Fonction pour stocker l'état actuel du jeu dans un fichier texte "saved_game.txt" pour pouvoir le charger plus tard
def save_game():
    with open("saved_game.txt", "w") as file:
        for row in game:
            file.write(",".join(map(str, row)) + "\n")
        file.write(str(score) + "\n")

# Fonction pour charger "saved_game.txt". Si le fichier existe, il lit l'état du jeu, le score, et met à jour l'affichage en conséquence.
# Si le fichier n'existe pas, il affiche un message d'erreur.
def load_game():
    try:
        with open("saved_game.txt", "r") as file:
            lines = file.readlines()
            for i in range(dp.GRID_LEN):
                game[i] = list(map(int, lines[i].strip().split(",")))
            global score
            score = int(lines[dp.GRID_LEN].strip())
            # Vérification si le 2048 a déja été atteint dans la partie sauvegardée et adapte la variable won en conséquence pour que le message de victoire ne
            # s'affiche pas immédiatement après le chargement de la partie si le 2048 a déjà été atteint ou est atteint à nouveau durant la reprise du jeu.
            global won
            won = check_win()
            update_grid()
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Aucune partie sauvegardée trouvée.")

btn_save = tk.Button(
    window,
    text="Sauvegarder",
    command=save_game,
    bg=dp.BACKGROUND_COLOR_GAME,
    width=12,
    height=2,
)
btn_save.place(x=600, y=120)

btn_load = tk.Button(
    window,
    text="Charger",
    command=load_game,
    bg=dp.BACKGROUND_COLOR_GAME,
    width=12,
    height=2,
)
btn_load.place(x=500, y=120)


# Fonction pour proposer une sauvegarde lorsqu'on tente de fermer la fenêtre. Si l'utilisateur choisit de sauvegarder, la fonction saved_game() est appelée avant de fermer la fenêtre.
# S'il choisit de ne pas sauvegarder, la fenêtre se ferme. S'il annule il peut continuer à jouer sans fermer la fenêtre.
def on_closing():
    response = messagebox.askyesnocancel(
        "Quitter",
        "Voulez-vous sauvegarder avant de quitter ?"
    )

    if response is True:
        # Oui → sauvegarder puis quitter
        save_game()
        window.destroy()

    elif response is False:
        # Non → quitter sans sauvegarder
        window.destroy()

    else:
        # Annuler → ne rien faire
        pass

window.protocol("WM_DELETE_WINDOW", on_closing)
# =========================================================
# 3. Fond de la grille
# =========================================================

frame_grille_bg = tk.Frame(
    window,
    bg=dp.BACKGROUND_COLOR_GRID,
    width=dp.SIZE,
    height=dp.SIZE
)
frame_grille_bg.place(x=334, y=245)

# =========================================================
# 4. Création des cellules
# =========================================================
label_grid = [[None, None, None, None],[None, None, None, None],[None, None, None, None],[None, None, None, None]]

for row in range(dp.GRID_LEN):
    for col in range(dp.GRID_LEN):

        label_grid[row][col] = tk.Label(
            frame_grille_bg,
            width=4,
            height=2,
            borderwidth=1,
            relief="solid",
            font=dp.FONT,
            bg=dp.BACKGROUND_COLOR_CELL_EMPTY
        )

        label_grid[row][col].grid(
            row=row,
            column=col,
            padx=dp.GRID_PADDING,
            pady=dp.GRID_PADDING
        )

# =========================================================
# 5. logique de mouvement
# =========================================================

def pack4(a,b,c,d):
    global score
    score_add=0 # détecte le nombre de mouvements effectués pendant le déplacement
    moves = 0
    # Si la 3ème case est vide mais la 4ème contient une valeur, alors on déplace la valeur de d vers c
    if c==0 and d!=0:
        moves += 1
        c,d= d,0
    # Si la 2ème case est vide mais la 3ème contient une valeur, alors on décale les valeurs vers la gauche
    if b == 0 and c!=0:
        moves += 1
        b, c, d = c, d, 0
    # Si la 1ère case est vide mais la 2ème contient une valeur, alors toute la ligne est décalée vers la gauche
    if a==0 and b!=0:
       moves += 1
       a,b,c,d=b,c,d,0
    # Si les deux premières cases ont la même valeur (et ne sont pas vides), alors elles fusionnent
    if a==b and a!=0 and b!=0:
       moves += 1
       a,b,c,d=a*2,c,d,0
       score_add += a # ajoute la valeur de la tuile créée lors de la fusion a score_add
    # Si les cases 2 et 3 ont la même valeur (et ne sont pas vides), alors elles fusionnent
    if b==c and b!=0 and c!=0:
        moves += 1
        b,c,d=b*2,d,0
        score_add += b # ajoute la valeur de la tuile créée lors de la fusion a score_add
    # Si les cases 3 et 4 ont la même valeur (et ne sont pas vides), alors elles fusionnent
    if c==d and c!=0 and d!=0:
        moves += 1
        c,d=c*2,0
        score_add += c # ajoute la valeur de la tuile créée lors de la fusion a score_add
    score += score_add
    return a,b,c,d, moves

def move_left():
    tot_moves=0
    for row in range(dp.GRID_LEN):
        game[row][0],game[row][1],game[row][2],game[row][3], moves = pack4(game[row][0], game[row][1], game[row][2], game[row][3])
        tot_moves += moves
    print(tot_moves)    #permet de vérifier le nombre de mouvements effectués pour faire le pack dans la console afin de s'assurer qu'il est correct.
    # Génération de la prochaine tuile et mise à jour de l'affichage de la grille et du score
    if tot_moves>0:
        tile_generator()
    update_grid()
    top_up()
    # Tests de fin de jeu
    check_end_game()
def move_right():
    tot_moves =0
    for row in range(dp.GRID_LEN):
        game[row][3],game[row][2],game[row][1],game[row][0],moves = pack4(game[row][3], game[row][2], game[row][1], game[row][0])
        tot_moves += moves
    print(tot_moves)    #permet de vérifier le nombre de mouvements effectués pour faire le pack dans la console afin de s'assurer qu'il est correct.
    # Génération de la prochaine tuile et mise à jour de l'affichage de la grille et du score
    if tot_moves > 0:
        tile_generator()
    update_grid()
    top_up()
    # Tests de fin de jeu
    check_end_game()
def move_up():
    tot_moves=0
    for col in range(dp.GRID_LEN):
        game[0][col],game[1][col],game[2][col],game[3][col],moves = pack4(game[0][col], game[1][col], game[2][col], game[3][col])
        tot_moves += moves
    print(tot_moves)    #permet de vérifier le nombre de mouvements effectués pour faire le pack dans la console afin de s'assurer qu'il est correct.
    # Génération de la prochaine tuile et mise à jour de l'affichage de la grille et du score
    if tot_moves > 0:
        tile_generator()
    update_grid()
    top_up()
    # Tests de fin de jeu
    check_end_game()
def move_down():
    tot_moves=0
    for col in range(dp.GRID_LEN):
        game[3][col],game[2][col],game[1][col],game[0][col],moves = pack4(game[3][col], game[2][col], game[1][col], game[0][col])
        tot_moves += moves
    print(tot_moves) #permet de vérifier le nombre de mouvements effectués pour faire le pack dans la console afin de s'assurer qu'il est correct.
    # Génération de la prochaine tuile et mise à jour de l'affichage de la grille et du score
    if tot_moves > 0:
        tile_generator()
    update_grid()
    top_up()
    # Tests de fin de jeu
    check_end_game()

def key_press(event):
    key= event.keysym
    global moves
    #moves est remis à 0 à chaque fois qu'une touche est pressée pour compter le nombre de mouvements effectués lors du pack
    moves=0
    print(moves)
    if key == dp.KEY_UP:
        print("up")
        move_up()
    elif key == dp.KEY_DOWN:
        print("down")
        move_down()
    elif key == dp.KEY_LEFT:
        print("left")
        move_left()
    elif key == dp.KEY_RIGHT:
        print("right")
        move_right()

window.bind('<Key>', key_press)

# Fonction qui ajoute la valeur de la tuile créée lors d'une fusion au score
def top_up():
# Fonction qui stocke le top score dans la variable top et l'écrit dans un fichier texte "top_score.txt" pour qu'il soit conservé même après la fermeture du jeu
    global top
    if score > top:
        top = score
        label_top.config(text=str(top))  # Met à jour l'affichage du top score
        with open("top_score.txt", "w") as file:
            file.write(str(top))

# =========================================================
# 6. Affichage de la tuile en fonction de sa valeur
# =========================================================
def tile_generator():
    # Cette fonction génère une nouvelle tuile (2 ou 4) dans une case vide de la grille après chaque mouvement.
    #La fonction vérifie d'abord s'il y a des cases vides dans la grille. Si c'est le cas, elle crée une liste de toutes les cases vides.
    empty_cells = []
    for row in range(dp.GRID_LEN):
        for col in range(dp.GRID_LEN):
            if game[row][col] == 0:
                empty_cells.append((row, col))
    # Si oui, elle choisit une case vide au hasard et y place une tuile avec une valeur de 2 ou 4 (80% de chances pour 2 et 20% pour 4).
    if empty_cells:
        row, col = random.choice(empty_cells)
        game[row][col] = 2 if random.random() < 0.8 else 4


def update_grid():
    label_score.config(text=str(score))  # Met à jour l'affichage du score
    for row in range(dp.GRID_LEN):
        for col in range(dp.GRID_LEN):

            value = game[row][col]

            if value == 0:

                label_grid[row][col].configure(
                    text="",
                    bg=dp.BACKGROUND_COLOR_CELL_EMPTY
                )

            else:

                label_grid[row][col].configure(
                    text=value,
                    bg=dp.BACKGROUND_COLOR_DICT[value],
                    fg=dp.CELL_COLOR_FG
                )

# =========================================================
# 7. États de test
# =========================================================

# Décommentez un seul bloc à la fois pour tester

# --- État initial ---
game=[
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

update_grid()
# =========================================================
# 8. Vérification de la victoire ou de la défaite
# =========================================================

# Fonction pour vérifier si le joueur a gagné (atteint la tuile 2048)
def check_win():
    global won
    for row in range(dp.GRID_LEN):
        for col in range(dp.GRID_LEN):
            if game[row][col] == 2048 and won == False:
                won = True
                return True
    return False
# Fonction pour vérifier s'il n'y a plus de mouvement possible (game over)
def check_game_over():
    for row in range(dp.GRID_LEN):
        for col in range(dp.GRID_LEN):
            # Vérifie si une tuile est à 0.
            if game[row][col] == 0:
                return False
            # Vérifie si deux tuiles adjacentes sont identiques (horizontalement et verticalement), ce qui permettrait une fusion.
            if col < dp.GRID_LEN - 1 and game[row][col] == game[row][col + 1]:
                return False
            if row < dp.GRID_LEN - 1 and game[row][col] == game[row + 1][col]:
                return False
    return True


# Fonction qui affiche le message de victoire et propose de continuer la partie ou de défaite et propose de recommencer une partie, ou de quitter le jeu.
def check_end_game():
    # Si check win() retourne True, cela signifie que le joueur a atteint la tuile 2048 et a gagné la partie.
    # Un message de victoire s'affiche avec une option pour continuer à jouer ou quitter le jeu.
    if check_win() :
        response = messagebox.askyesno("Victoire", "Félicitations, vous avez gagné ! Voulez-vous continuer à jouer ?")
        if not response:
            window.destroy()
    # Si check_game_over() retourne True, cela signifie que le joueur n'a plus de mouvements possibles et a perdu la partie.
    # Un message de défaite s'affiche avec une option pour recommencer une partie ou quitter le jeu.
    elif check_game_over():
        response = messagebox.askyesno("Game Over", "Désolé, vous avez perdu ! Voulez-vous recommencer une partie ?")
        if response:
            new_game()
        else:
            window.destroy()

# =========================================================
# 9. Boucle principale de la fenêtre tkinter
# =========================================================
new_game()
window.mainloop()