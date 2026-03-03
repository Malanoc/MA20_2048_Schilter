#DisplayParam est un module qui contient les paramètres d'affichage pour le jeu 2048.
#Il définit les couleurs de fond, les couleurs des cellules, la police et les touches de contrôle.
#Ces paramètres sont utilisés dans le fichier principal 2048.py pour créer l'interface graphique du jeu.

SIZE = 500
GRID_LEN = 4
GRID_PADDING = 8

BACKGROUND_COLOR_GAME = "#ACABAB"
BACKGROUND_COLOR_GRID = "#D9D9D9"
BACKGROUND_COLOR_CELL_EMPTY = "#A4A19E"

BACKGROUND_COLOR_DICT = {
2: "#FFFFFF",
4: "#F8ECE0",
8: "#F5DCC4",
16:"#F8D1AA",
32: "#F4B97F",
64: "#F6A95F",
128: "#FA9631",
256: "#FF8102",
512: "#C36507",
1024: "#CF5408",
2048: "#ED4217",
4096: "#F01010",
8192: "#CE2727",
}

CELL_COLOR_FG = "#000000"

FONT = ("Arial",40,"bold")


KEY_UP = "Up" or "w" or "W"
KEY_DOWN = "Down" or "s" or "S"
KEY_LEFT = "Left" or "a" or "A"
KEY_RIGHT = "Right" or "d" or "D"