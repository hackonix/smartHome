import tkinter as tk
from tkinter import ttk


# -----------------------------
# KONSTANTE
# -----------------------------
FONT_TITLE = ("Arial", 22)
FONT_SUBTITLE = ("Arial", 18)
FONT_POSTAVKE = ("Arial", 16)
FONT_STANDARD = ("Arial", 14)

RASVJETA_PLACEHOLDER = "UPRAVLJANJE RASVJETOM"
TEMPERATURA_PLACEHOLDER = "UPRAVLJANJE TEMPERATUROM"
KAMERA_PLACEHOLDER = "UPRAVLJANJE KAMEROM"
DODATNE_METRIKE_PLACEHOLDER = "UPRAVLJAJ DODATNIM MJERENJIMA"
LOKACIJA_PLACEHOLDER = "UPRAVLJAJ LOKACIJOM"


class FirstScreen:
    def __init__(self, root: tk.Tk, screen_size: str = "600x400") -> None:
        self.root = root
        self.root.title = "SmartHome"
        self.root.geometry(screen_size)

        # -----------------------------
        # SCREEN POSTAVKE
        # -----------------------------

        self.label_postavke = ttk.Label(
            self.root, text="POSTAVKE SUSTAVA", font=FONT_TITLE
        )
        self.label_postavke.place(relx=0.5, rely=0.05, anchor="center")

        # -----------------------------
        # MOGUCE POSTAVKE
        # -----------------------------
        BUTTON_WIDTH = 500
        FIRST_REL_Y_PLACEMENT = 0.15
        # Upravljanje rasvjetom - button
        self.button_upravljanje_rasvjetom = ttk.Button(
            self.root,
            text=RASVJETA_PLACEHOLDER,
        )
        self.button_upravljanje_rasvjetom.place(
            relx=0.5, rely=FIRST_REL_Y_PLACEMENT, width=BUTTON_WIDTH, anchor="center"
        )

        # Upravljanje temperaturom - button
        self.button_upravljanje_temperaturom = ttk.Button(
            self.root, text=TEMPERATURA_PLACEHOLDER
        )
        self.button_upravljanje_temperaturom.place(
            relx=0.5,
            rely=(FIRST_REL_Y_PLACEMENT + 0.075 * 1),
            width=BUTTON_WIDTH,
            anchor="center",
        )
