# Projet: 2048- MA-20 - 2026
# Auteur: Marc Schilter - SI-CA1a
# Ce projet est une implémentation du jeu 2048 en Python.
# Le but du jeu est de faire glisser les tuiles sur une grille pour combiner les tuiles de même valeur et atteindre la tuile 2048.

import tkinter as tk
import  DisplayParam as dp

window = tk.Tk()
window.title("2048")
window.geometry("1168x990")
window.resizable(False, False)
window.configure(bg=dp.BACKGROUND_COLOR_GAME)


frame_grille_bg = tk.Frame(window, bg=dp.BACKGROUND_COLOR_GRID, width=dp.SIZE, height=dp.SIZE)
frame_grille_bg.place(x=334, y=245)

for line in range(dp.GRID_LEN):
    for column in range(dp.GRID_LEN):
        frame_cell = tk.Frame(frame_grille_bg, bg=dp.BACKGROUND_COLOR_CELL_EMPTY, width=dp.SIZE/dp.GRID_LEN, height=dp.SIZE/dp.GRID_LEN, )
        frame_cell.grid(row=line, column=column, padx=dp.GRID_PADDING, pady=dp.GRID_PADDING)













window.mainloop()