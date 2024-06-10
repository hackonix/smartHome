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

ZELJENI_EVENT = "<Button-1>"


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
            ZELJENI_EVENT,
            self.button_rasvjeta_on_click,
        )

        self.button_upravljanje_temperaturom.bind(
            ZELJENI_EVENT,
            self.button_temp_on_click,
        )

        self.button_upravljanje_kamerom.bind(
            ZELJENI_EVENT,
            self.button_kamera_on_click,
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

    # -----------------------------
    # PROMIJENI SCREEN
    # -----------------------------

    def button_rasvjeta_on_click(self, event):
        RasvjetaScreen(self.root)

    def button_temp_on_click(self, event):
        TemperaturaScreen(self.root)

    def button_kamera_on_click(self, event):
        KameraScreen(self.root)


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
            self.rasvjeta_postavke,
            text="Spremi",
            command=self.spremanje_postavki_rasvjete,
        )
        save_button.pack(pady=20)

        # -----------------------------
        # FUNKCIJE SECOND SCREEN
        # -----------------------------

    def spremanje_postavki_rasvjete(self):
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


class TemperaturaScreen(MainMenu):
    def __init__(self, root: tk.Tk, screen_size: str = "800x300") -> None:
        super().__init__(root, screen_size)
        self.root = root
        self.title = "Temperatura - Postavke"

        self.temperatura_postavke = tk.Frame(self.root, borderwidth=2, relief="groove")

        self.temperatura_postavke.place(x=200, y=50, width=300, height=200)

        # Oznaka i unos temperature
        tk.Label(self.temperatura_postavke, text="Zeljena temperatura: ").pack(pady=10)

        self.zeljena_temperatura = tk.StringVar()
        self.zeljena_temperatura_entry = ttk.Entry(
            self.temperatura_postavke, textvariable=self.zeljena_temperatura
        )
        self.zeljena_temperatura_entry.pack(pady=5)

        save_button = ttk.Button(
            self.temperatura_postavke,
            text="Spremi",
            command=self.spremanje_postavki_temperature,
        )
        save_button.pack(pady=20)

    def spremanje_postavki_temperature(self):
        self.zeljena_temperatura = self.zeljena_temperatura.get()
        self.temperatura_postavke.destroy()


class KameraScreen(MainMenu):
    def __init__(self, root: tk.Tk, screen_size: str = "800x300") -> None:
        super().__init__(root, screen_size)

        self.root = root
        self.title = "Kamera - Postavke"

        self.kamera_postavke = tk.Frame(self.root, borderwidth=2, relief="groove")

        self.kamera_postavke.place(
            x=200, y=50, width=300, height=200
        )  # Postavljanje okvira unutar glavnog prozora

        # Checkbox za automatsko paljenje po zalasku sunca
        self.kamera_var = tk.BooleanVar()
        tk.Checkbutton(
            self.kamera_postavke,
            text="Ukljuci/iskljuci kameru",
            variable=self.kamera_var,
        ).pack(pady=10)

        # Oznaka i unos za sat kad će se svjetlo upaliti
        tk.Label(
            self.kamera_postavke, text="Upali/iskljuci kameru u (HH:MM) - (HH:MM):"
        ).pack(pady=10)

        self.kamera_hour = tk.StringVar()
        self.kamera_hour_entry = ttk.Entry(
            self.kamera_postavke, textvariable=self.kamera_hour
        )
        self.kamera_hour_entry.pack(pady=5)

        self.kamera_save_button = ttk.Button(
            self.kamera_postavke,
            text="Spremi",
            command=self.spremanje_postavki_kamere,
        )
        self.kamera_save_button.pack(pady=20)

    def spremanje_postavki_kamere(self):
        if self.kamera_var.get():
            self.kamera_ON = True
            self.kamera_postavke.destroy()
            return "00:00 - 23:59"

        else:
            self.kamera_hour = self.kamera_hour.get()
            self.kamera_postavke.destroy()
            return self.kamera_hour
