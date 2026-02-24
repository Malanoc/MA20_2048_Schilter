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
# 4. Création des cellules uniquement avec des labels
# =========================================================

cell_labels = []

cell_size = dp.SIZE // dp.GRID_LEN

for x in range(dp.GRID_LEN):

    cell_labels.append([])

    for y in range(dp.GRID_LEN):

        pos_x = y * cell_size + dp.GRID_PADDING
        pos_y = x * cell_size + dp.GRID_PADDING

        cell_label = tk.Label(
            frame_grille_bg,
            text="",
            font=dp.FONT,
            fg="#000000",
            bg=dp.BACKGROUND_COLOR_CELL_EMPTY
        )

        cell_label.place(
            x=pos_x,
            y=pos_y,
            width=cell_size - 2*dp.GRID_PADDING,
            height=cell_size - 2*dp.GRID_PADDING
        )

        cell_labels[x].append(cell_label)



# =========================================================
# 5. Affichage de la tuile en fonction de sa valeur
# =========================================================

def update_grid():
    for x in range(dp.GRID_LEN):
        for y in range(dp.GRID_LEN):

            value = game[x][y]
            label = cell_labels[x][y]

            if value == 0:

                label.config(
                    text="",
                    bg=dp.BACKGROUND_COLOR_CELL_EMPTY
                )

            else:

                label.config(
                    text=str(value),
                    fg=dp.CELL_COLOR_DICT[value],
                    bg=dp.BACKGROUND_COLOR_DICT[value]
                )


# =========================================================
# 6. États de test
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
game = [
    [2, 4, 8, 16],
    [32, 64, 128, 256],
    [512, 1024, 2048, 4096],
    [8192, 0, 0, 0]
]

update_grid()


# =========================================================
# 7. Boucle principale de la fenêtre tkinter
# =========================================================



def pack4(a,b,c,d):
    if c==0:
        c,d= d,0
    if b == 0:
        b, c, d = c, d, 0
    if a==0:
       a,b,c,d=b,c,d,0
    if a==b:
        a,b,c,d=a*2,c,d,0
    if b==c:
        b,c,d=b*2,d,0
    if c==d:
        c,d=c*2,0
    return (a,b,c,d)

print(pack4(0,0,0,2))
print(pack4(0,0,2,2))
print(pack4(2,0,2,2))
print(pack4(2,2,2,2))
print(pack4(2,2,4,0))

a= input("")
b= input("")
c= input("")
d= input("")

print(pack4(int(a),int(b),int(c),int(d)))

window.mainloop()