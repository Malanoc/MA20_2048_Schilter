# Projet: 2048- MA-20 - 2026
# Auteur: Marc Schilter - SI-CA1a
# Ce projet est une implémentation du jeu 2048 en Python.
# Le but du jeu est de faire glisser les tuiles sur une grille pour combiner les tuiles de même valeur et atteindre la tuile 2048.

import tkinter as tk
import  DisplayParam as dp

# =========================================================
# 1. Fenêtre principale
# =========================================================

window = tk.Tk()
window.title("2048")
window.geometry("1168x990")
window.resizable(False, False)
window.configure(bg=dp.BACKGROUND_COLOR_GAME)


# =========================================================
# 2. Variables mémoire du jeu
# =========================================================

# Grille logique (0 = vide)
game = [
    [2, 4, 8, 16],
    [32, 64, 128, 256],
    [512, 1024, 2048, 4096],
    [8192, 0, 0, 0]
]

score = 0


# =========================================================
# 3. Interface supérieure (titre, score, bouton)
# =========================================================

# Titre du jeu
label_title = tk.Label(
    window,
    text="2048",
    font=("Arial", 48, "bold"),
    bg=dp.BACKGROUND_COLOR_GAME
)
label_title.place(x=500, y=40)

# Texte "Score"
label_score_title = tk.Label(
    window,
    text="Score",
    font=("Arial", 14),
    bg=dp.BACKGROUND_COLOR_GAME
)
label_score_title.place(x=540, y=120)

# Affichage du score
label_score = tk.Label(
    window,
    text=str(score),
    font=("Arial", 20, "bold"),
    bg="white",
    width=6
)
label_score.place(x=520, y=145)

# Bouton nouveau jeu
def new_game():
    global game, score
    score = 0
    label_score.config(text=str(score))

    game = [[0] * dp.GRID_LEN for _ in range(dp.GRID_LEN)]
    update_grid()

btn_new = tk.Button(
    window,
    text="Nouveau",
    command=new_game
)
btn_new.place(x=535, y=190)


# =========================================================
# 4. Fond de la grille
# =========================================================

frame_grille_bg = tk.Frame(
    window,
    bg=dp.BACKGROUND_COLOR_GRID,
    width=dp.SIZE,
    height=dp.SIZE
)
frame_grille_bg.place(x=334, y=245)


# =========================================================
# 5. Structures graphiques miroir
# =========================================================

cell_frames = [
    [None for _ in range(dp.GRID_LEN)]
    for _ in range(dp.GRID_LEN)
]

cell_labels = [
    [None for _ in range(dp.GRID_LEN)]
    for _ in range(dp.GRID_LEN)
]

cell_size = dp.SIZE // dp.GRID_LEN


# =========================================================
# 6. Création des cellules
# =========================================================

for i in range(dp.GRID_LEN):
    for j in range(dp.GRID_LEN):
        # Tuile (Frame coloré)
        cell_frame = tk.Frame(
            frame_grille_bg,
            bg=dp.BACKGROUND_COLOR_CELL_EMPTY,
            width=cell_size,
            height=cell_size
        )
        cell_frame.grid(
            row=i,
            column=j,
            padx=dp.GRID_PADDING,
            pady=dp.GRID_PADDING
        )
        cell_frame.grid_propagate(False)

        # Texte de la tuile
        label = tk.Label(
            cell_frame,
            text="",
            font=dp.FONT,
            fg="#000000",
            bg=dp.BACKGROUND_COLOR_CELL_EMPTY
        )
        label.place(relx=0.5, rely=0.5, anchor="center")

        cell_frames[i][j] = cell_frame
        cell_labels[i][j] = label


# =========================================================
# 7. Synchronisation logique → affichage
# =========================================================

def update_grid():
    #Met à jour l'affichage selon la variable game
    for i in range(dp.GRID_LEN):
        for j in range(dp.GRID_LEN):
            value = game[i][j]
            frame = cell_frames[i][j]
            label = cell_labels[i][j]

            if value == 0:
                frame.config(bg=dp.BACKGROUND_COLOR_CELL_EMPTY)
                label.config(
                    text="",
                    bg=dp.BACKGROUND_COLOR_CELL_EMPTY
                )
            else:
                color_bg = dp.BACKGROUND_COLOR_DICT[value]
                color_fg = dp.CELL_COLOR_DICT[value]

                frame.config(bg=color_bg)
                label.config(
                    text=str(value),
                    fg=color_fg,
                    bg=color_bg
                )


# =========================================================
# 8. Affichage initial
# =========================================================

update_grid()


# =========================================================
# 9. Boucle principale
# =========================================================

window.mainloop()