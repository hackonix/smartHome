import tkinter as tk
import requests
from tkinter import ttk
from datetime import datetime


# -----------------------------
# KONSTANTE
# -----------------------------
FONT_TITLE = ("Arial", 22)
FONT_SUBTITLE = ("Arial", 18)
FONT_POSTAVKE = ("Arial", 16)
FONT_STANDARD = ("Arial", 14)

RASVJETA_PLACEHOLDER = "RASVJETA"
TEMPERATURA_PLACEHOLDER = "TEMP"
KAMERA_PLACEHOLDER = "KAMERA"
VLAZNOST_PLACEHOLDER = "VLAZNOST"
TLAK_PLACEHOLDER = "TLAK"
LOKACIJA_PLACEHOLDER = "LOKACIJA"


class MainMenu:
    def __init__(self, root: tk.Tk, screen_size: str = "800x300") -> None:
        self.root = root
        self.root.title = "SmartHome"
        self.root.geometry(screen_size)

        self.lokacija = "Zagreb"

        # -----------------------------
        # PRIKAZ DATUMA
        # -----------------------------
        self.label_datum = tk.Label(root, text="Datum, loading...")
        self.label_datum.place(relx=0.025, rely=0.05, anchor="w")
        # TODO: Napraviti funkciju koja update-a self.label_datum

        # -----------------------------
        # PRIKAZ VANJESKE TEMPERATURE
        # -----------------------------
        self.label_vanjska_temp = tk.Label(root, text="Vanjska temperatura, loading...")
        self.label_vanjska_temp.place(relx=0.95, rely=0.05, anchor="e")
        # TODO: Napraviti funkciju koja update-a self.label_vanjska_temp

        # -----------------------------
        # GLAVNI IZBORNIK
        # -----------------------------

        self.label_postavke = ttk.Label(
            self.root, text="GLAVNI IZBORNIK", font=FONT_TITLE
        )
        self.label_postavke.place(relx=0.5, rely=0.15, anchor="center")

        # -----------------------------
        # MOGUCE POSTAVKE
        # -----------------------------
        BUTTON_WIDTH = 75
        BUTTON_HEIGHT = 75

        # Upravljanje rasvjetom - button
        self.button_upravljanje_rasvjetom = tk.Button(
            self.root,
            text=RASVJETA_PLACEHOLDER,
        )
        self.button_upravljanje_rasvjetom.place(
            relx=0.25,
            rely=0.25,
            height=BUTTON_HEIGHT,
            width=BUTTON_WIDTH,
        )

        # Upravljanje temperaturom - button
        self.button_upravljanje_temperaturom = tk.Button(
            self.root,
            text=TEMPERATURA_PLACEHOLDER,
        )
        self.button_upravljanje_temperaturom.place(
            relx=0.35,
            rely=0.25,
            height=BUTTON_HEIGHT,
            width=BUTTON_WIDTH,
        )

        # Upravljanje kamerom - button
        self.button_upravljanje_kamerom = tk.Button(
            self.root,
            text=KAMERA_PLACEHOLDER,
        )
        self.button_upravljanje_kamerom.place(
            relx=0.45,
            rely=0.25,
            height=BUTTON_HEIGHT,
            width=BUTTON_WIDTH,
        )

        # Upravljanje vlaznost - button
        self.button_upravljanje_vlaznost = tk.Button(
            self.root,
            text=VLAZNOST_PLACEHOLDER,
        )
        self.button_upravljanje_vlaznost.place(
            relx=0.55,
            rely=0.25,
            height=BUTTON_HEIGHT,
            width=BUTTON_WIDTH,
        )

        # Upravljanje tlak - button
        self.button_upravljanje_tlak = tk.Button(self.root, text=TLAK_PLACEHOLDER)
        self.button_upravljanje_tlak.place(
            relx=0.65,
            rely=0.25,
            height=BUTTON_HEIGHT,
            width=BUTTON_WIDTH,
        )

        # TODO: Dodati click eventove za svaki button - svaki button vodi na novi screen, osim vlaznosti i tlaka, oni samo prikazuju vrijednosti

        # -----------------------------
        # UPDATE-AJ PODATKE
        # -----------------------------
        self.root.after(1000, self.update_time)
        self.root.after(1000, self.update_out_temp)

        # -----------------------------
        # CONFIGURE EVENTS
        # -----------------------------
        self.button_upravljanje_rasvjetom.bind(
            "<Button-1>", self.button_rasvjeta_on_click
        )

    # -----------------------------
    # FUNKCIJE ZA FIRST SCREEN
    # -----------------------------

    def update_time(self):
        trenutno_vrijeme = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.label_datum.config(text=f"{trenutno_vrijeme}")
        self.root.after(1000, self.update_time)

    def update_out_temp(self):
        Api_Key = "2606f769271b8d545fe3458b2b72ed9f"
        final_URL = f"http://api.openweathermap.org/data/2.5/weather?q={self.lokacija}&appid={Api_Key}&units=metric"
        try:
            response = requests.get(final_URL)
            response.raise_for_status()
            data = response.json()
            temperature = data["main"]["temp"]
            lokacija_display = self.lokacija
            self.label_vanjska_temp.configure(
                text=f"Temperatura u mjestu {lokacija_display}: {temperature}°C"
            )
        except requests.exceptions.RequestException as e:
            self.label_vanjska_temp.configure(text=f"Greska: {e}")
        self.root.after(5000, self.update_out_temp)

    # OCISTI WIDGETE KOD PROMJENE SCREENA
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy

    # -----------------------------
    # PROMIJENI SCREEN
    # -----------------------------

    def button_rasvjeta_on_click(self, event):
        self.clear_screen()
        RasvjetaScreen(self.root)


class RasvjetaScreen(MainMenu):
    def __init__(self, root: tk.Tk, screen_size: str = "800x300") -> None:
        super().__init__(root, screen_size)
        self.root = root
        self.title = "Postavke rasvjete"

        self.rasvjeta_postavke = tk.Frame(self.root, borderwidth=2, relief="groove")

        self.rasvjeta_postavke.place(
            x=200, y=50, width=300, height=200
        )  # Postavljanje okvira unutar glavnog prozora

        # Checkbox za automatsko paljenje po zalasku sunca
        self.sunset_var = tk.BooleanVar()
        tk.Checkbutton(
            self.rasvjeta_postavke,
            text="Automatski upali po zalasku sunca",
            variable=self.sunset_var,
        ).pack(pady=10)

        # Oznaka i unos za sat kad će se svjetlo upaliti
        tk.Label(self.rasvjeta_postavke, text="Upali svjetlo u (HH:MM):").pack(pady=10)

        hour_var = tk.StringVar()
        hour_entry = ttk.Entry(self.rasvjeta_postavke, textvariable=hour_var)
        hour_entry.pack(pady=5)

        save_button = ttk.Button(
            self.rasvjeta_postavke, text="Spremi", command=self.spremanje_postavki
        )
        save_button.pack(pady=20)

        # -----------------------------
        # FUNKCIJE SECOND SCREEN
        # -----------------------------

    def spremanje_postavki(self):
        if self.sunset_var.get():
            vrijeme_zalaska = self.zalazak_sunca()
            if vrijeme_zalaska:
                print(
                    f"Svjetlo će se automatski upaliti po zalasku sunca u: {vrijeme_zalaska}"
                )

        else:
            self.hour = self.hour_var.get()
            print(f"Svjetlo će se upaliti u: {hour} sati")
        self.rasvjeta_postavke.destroy()

    def zalazak_sunca(self):
        response = requests.get(
            f"https://hr.meteocast.net/sunrise-sunset/hr/zagreb/#google_vignette"
        )

        return response


class TemperaturaMenu(MainMenu):
    def __init__(self, root: tk.Tk, screen_size: str = "800x300") -> None:
        super().__init__(root, screen_size)
        pass
