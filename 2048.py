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
score_add = 0

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
    global moves, score_add # détecte le nombre de mouvements effectués pendant le déplacement

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
    return (a,b,c,d)

def move_left():
    for row in range(dp.GRID_LEN):
        game[row][0],game[row][1],game[row][2],game[row][3] = pack4(game[row][0], game[row][1], game[row][2], game[row][3])
    print(moves)    #permet de vérifier le nombre de mouvements effectués pour faire le pack dans la console afin de s'assurer qu'il est correct.
    # Génération de la prochaine tuile et mise à jour de l'affichage de la grille et du score
    tile_generator()
    update_grid()
    score_up()
    # Tests de fin de jeu
    check_end_game()
def move_right():
    for row in range(dp.GRID_LEN):
        game[row][3],game[row][2],game[row][1],game[row][0] = pack4(game[row][3], game[row][2], game[row][1], game[row][0])
    print(moves)    #permet de vérifier le nombre de mouvements effectués pour faire le pack dans la console afin de s'assurer qu'il est correct.
    # Génération de la prochaine tuile et mise à jour de l'affichage de la grille et du score
    tile_generator()
    update_grid()
    score_up()
    # Tests de fin de jeu
    check_end_game()
def move_up():
    for col in range(dp.GRID_LEN):
        game[0][col],game[1][col],game[2][col],game[3][col] = pack4(game[0][col], game[1][col], game[2][col], game[3][col])
    print(moves)    #permet de vérifier le nombre de mouvements effectués pour faire le pack dans la console afin de s'assurer qu'il est correct.
    # Génération de la prochaine tuile et mise à jour de l'affichage de la grille et du score
    tile_generator()
    update_grid()
    score_up()
    # Tests de fin de jeu
    check_end_game()
def move_down():
    for col in range(dp.GRID_LEN):
        game[3][col],game[2][col],game[1][col],game[0][col] = pack4(game[3][col], game[2][col], game[1][col], game[0][col])
    print(moves) #permet de vérifier le nombre de mouvements effectués pour faire le pack dans la console afin de s'assurer qu'il est correct.
    # Génération de la prochaine tuile et mise à jour de l'affichage de la grille et du score
    tile_generator()
    update_grid()
    score_up()
    # Tests de fin de jeu
    check_end_game()

def key_press(event):
    key= event.keysym
    global moves, score_add
    #moves est remis à 0 à chaque fois qu'une touche est pressée pour compter le nombre de mouvements effectués lors du pack
    moves=0
    score_add=0
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
def score_up():
    global score, score_add
    # Ajoute score_add au score total et met à jour l'affichage du score
    score += score_add
    label_score.config(text=str(score))  # Met à jour l'affichage du score

# =========================================================
# 6. Affichage de la tuile en fonction de sa valeur
# =========================================================
def tile_generator():
    # Cette fonction génère une nouvelle tuile (2 ou 4) dans une case vide de la grille après chaque mouvement.
    if moves !=0:   # la tuile ne se génère que si un mouvement a été effectué (moves>0)
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




# --- Toutes les tuiles ---
#game = [
#    [2, 4, 8, 16],
#    [32, 64, 128, 256],
#    [512, 1024, 2048, 4096],
#    [8192, 0, 0, 0]
#]
# --- Tuiles à combiner pour test ---
#game = [
#    [2, 2, 4, 4],
#    [4, 0, 4, 0],
#    [4, 4, 2, 0],
#    [2, 4, 0, 2]
#]

update_grid()

# Tests pour la fonction pack4
#print(pack4(0,0,0,2))
#print(pack4(0,0,2,2))
#print(pack4(2,0,2,2))
#print(pack4(2,2,2,2))
#print(pack4(2,2,4,0))
#print ("donnez moi 4 chiffres pour tester la fonction pack4")
#a= input("")
#b= input("")
#c= input("")
#d= input("")

#print(pack4(int(a),int(b),int(c),int(d)))
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