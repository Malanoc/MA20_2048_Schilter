# ================================================================================================================================
# Projet: 2048- MA-20 - 2026
# Auteur: Marc Schilter - SI-CA1a
# Description: Ce projet est une implémentation du jeu 2048 en Python.
# Le but du jeu est de faire glisser les tuiles sur une grille pour combiner les tuiles de même valeur et atteindre la tuile 2048.
# ================================================================================================================================

import tkinter as tk
import  DisplayParam as dp

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
label_score_title.place(x=710, y=105)

score=0

label_score = tk.Label(
    window,
    text=str(score),
    font=("Arial", 16, "bold"),
    bg=dp.BACKGROUND_COLOR_GRID,
    width=6
)
label_score.place(x=710, y=145)

label_top_title = tk.Label(
    window,
    text="Top",
    font=("Arial", 16, "bold"),
    bg=dp.BACKGROUND_COLOR_GRID,
    width=6,
    height=2,
)
label_top_title.place(x=815, y=105)

top =0

label_top = tk.Label(
    window,
    text=str(top),
    font=("Arial", 16, "bold"),
    bg=dp.BACKGROUND_COLOR_GRID,
    width=6
)
label_top.place(x=815, y=145)

def new_game():
    global game, score
    score = 0
    label_score.config(text=str(score))

    game = [[0] * dp.GRID_LEN for _ in range(dp.GRID_LEN)]
    update_grid()

btn_new = tk.Button(
    window,
    text="Nouveau",
    command=new_game,
    bg=dp.BACKGROUND_COLOR_GAME,
    width=12,
    height=2,
)
btn_new.place(x=805, y=190)


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
    global moves  #détecte le nombre de mouvements effectués pour faire le pack
    if c==0 and d!=0:
        moves += 1
        c,d= d,0
    if b == 0 and c!=0:
        moves += 1
        b, c, d = c, d, 0
    if a==0 and b!=0:
       moves += 1
       a,b,c,d=b,c,d,0
    if a==b and a!=0 and b!=0:
       moves += 1
       a,b,c,d=a*2,c,d,0
    if b==c and b!=0 and c!=0:
        moves += 1
        b,c,d=b*2,d,0
    if c==d and c!=0 and d!=0:
        moves += 1
        c,d=c*2,0
    return (a,b,c,d)

def move_left():
    for row in range(dp.GRID_LEN):
        game[row][0],game[row][1],game[row][2],game[row][3] = pack4(game[row][0], game[row][1], game[row][2], game[row][3])
    print(moves)
    update_grid()
def move_right():
    for row in range(dp.GRID_LEN):
        game[row][3],game[row][2],game[row][1],game[row][0] = pack4(game[row][3], game[row][2], game[row][1], game[row][0])
    print(moves)
    update_grid()
def move_up():
    for col in range(dp.GRID_LEN):
        game[0][col],game[1][col],game[2][col],game[3][col] = pack4(game[0][col], game[1][col], game[2][col], game[3][col])
    print(moves)
    update_grid()
def move_down():
    for col in range(dp.GRID_LEN):
        game[3][col],game[2][col],game[1][col],game[0][col] = pack4(game[3][col], game[2][col], game[1][col], game[0][col])
    print(moves)
    update_grid()

def key_press(event):
    key= event.keysym
    global moves
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

# =========================================================
# 6. Affichage de la tuile en fonction de sa valeur
# =========================================================

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
#game = [
#     [0, 0, 0, 0],
#     [0, 0, 2, 0],
#     [0, 0, 0, 0],
#     [2, 0, 0, 0]
#]

# --- Toutes les tuiles ---
#game = [
#    [2, 4, 8, 16],
#    [32, 64, 128, 256],
#    [512, 1024, 2048, 4096],
#    [8192, 0, 0, 0]
#]
# --- Tuiles à combiner ---
game = [
    [2, 2, 4, 4],
    [4, 0, 4, 0],
    [4, 4, 2, 0],
    [2, 4, 0, 2]
]




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
# 8. Boucle principale de la fenêtre tkinter
# =========================================================
window.mainloop()