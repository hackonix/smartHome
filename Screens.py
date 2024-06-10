import tkinter as tk
import requests
from tkinter import ttk
from datetime import datetime
from PIL import Image, ImageTk
import cv2


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
DODATNE_METRIKE_PLACEHOLDER = "DOD.\nMJER."
GLAVNI_PRIKAZ_PLACEHOLDER = "GLAVNI\nPRIKAZ"
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
        self.button_upravljanje_dodatne_metrike = tk.Button(
            self.root,
            text=DODATNE_METRIKE_PLACEHOLDER,
        )
        self.button_upravljanje_dodatne_metrike.place(
            relx=0.55,
            rely=0.25,
            height=BUTTON_HEIGHT,
            width=BUTTON_WIDTH,
        )

        # Upravljanje tlak - button
        self.button_glavni_prikaz = tk.Button(self.root, text=GLAVNI_PRIKAZ_PLACEHOLDER)
        self.button_glavni_prikaz.place(
            relx=0.65,
            rely=0.25,
            height=BUTTON_HEIGHT,
            width=BUTTON_WIDTH,
        )

        # TODO: Dodati click eventove za svaki button - svaki button vodi na novi screen, osim vlaznosti i tlaka, oni samo prikazuju vrijednosti

        # -----------------------------
        # UPDATE-AJ PODATKE
        # -----------------------------
        self.root.after(1000, self.update_time_mainMenu)
        self.root.after(1000, self.update_out_temp_mainMenu)

        # -----------------------------
        # EVENT BINDING
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

        self.button_upravljanje_dodatne_metrike.bind(
            ZELJENI_EVENT,
            self.button_dodatne_metrike_on_click,
        )

        self.button_glavni_prikaz.bind(
            ZELJENI_EVENT,
            self.button_glavni_prikaz_on_click,
        )

    # -----------------------------
    # FUNKCIJE ZA MAIN MENU
    # -----------------------------

    def update_time_mainMenu(self):
        trenutno_vrijeme = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.label_datum.config(text=f"{trenutno_vrijeme}")
        self.root.after(1000, self.update_time_mainMenu)

    def update_out_temp_mainMenu(self):
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
        self.root.after(5000, self.update_out_temp_mainMenu)

    # -----------------------------
    # PROMIJENI SCREEN
    # -----------------------------

    def button_rasvjeta_on_click(self, event):
        global Rasvjeta
        Rasvjeta = RasvjetaScreen(self.root)

    def button_temp_on_click(self, event):
        global Temperatura
        Temperatura = TemperaturaScreen(self.root)

    def button_kamera_on_click(self, event):
        global Kamera
        Kamera = KameraScreen(self.root)

    def button_dodatne_metrike_on_click(self, event):
        global DodatneMetrike
        DodatneMetrike = DodatneMetrikeScreen(self.root)

    def button_glavni_prikaz_on_click(self, event):
        self.root.destroy()
        global GlavniPrikaz
        GlavniPrikaz = GlavniPrikazScreen(self.root)


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
            self.vrijeme_zalaska = self.zalazak_sunca()
        else:
            self.hour = self.hour_var.get()
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
            self.kamera_hour = "00:00 - 23:59"
        else:
            self.kamera_hour = self.kamera_hour.get()

        self.kamera_postavke.destroy()


class DodatneMetrikeScreen(MainMenu):
    def __init__(self, root: tk.Tk, screen_size: str = "800x300") -> None:
        super().__init__(root, screen_size)
        self.root = root
        self.title = "Doodatne metrike - postavke"

        self.dodatne_metrike_postavke = tk.Frame(
            self.root, borderwidth=2, relief="groove"
        )

        self.dodatne_metrike_postavke.place(
            x=200, y=50, width=300, height=200
        )  # Postavljanje okvira unutar glavnog prozora

        # Checkbox za automatsko paljenje po zalasku sunca
        self.vlaznost_var = tk.BooleanVar()
        self.tlak_var = tk.BooleanVar()

        tk.Checkbutton(
            self.dodatne_metrike_postavke,
            text="Prikaz vlaznosti zraka",
            variable=self.vlaznost_var,
        ).pack(pady=10)

        tk.Checkbutton(
            self.dodatne_metrike_postavke,
            text="Prikaz tlaka zraka",
            variable=self.tlak_var,
        ).pack(pady=10)

        self.dodatne_metrike_save_button = ttk.Button(
            self.dodatne_metrike_postavke,
            text="Spremi",
            command=self.spremanje_postavki_dodatne_metrike,
        )
        self.dodatne_metrike_save_button.pack(pady=20)

    def spremanje_postavki_dodatne_metrike(self):
        if self.vlaznost_var.get():
            self.vlaznost_var = self.vlaznost_var.get()

        if self.tlak_var.get():
            self.tlak_var = self.tlak_var.get()

        self.dodatne_metrike_postavke.destroy()


class GlavniPrikazScreen(
    RasvjetaScreen, TemperaturaScreen, KameraScreen, DodatneMetrikeScreen, MainMenu
):
    def __init__(self, root: tk.Tk, screen_size: str = "800x600") -> None:

        self.root = tk.Tk()
        self.title = "Glavni prikaz"
        self.root.geometry(screen_size)

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        # -----------------------------
        # RASVJETA LABEL
        # MIJENJA BOJU OVISNO O VREMENU
        # -----------------------------

        # -----------------------------
        # VIDEO FRAME LABEL
        # -----------------------------

        # TODO: If kamera_var ili trenutno vrijeme u kamera_hour range-u onda bi se ovo trebalo prikazivati, inace ne
        # Implementirati funkcionalnost

        self.video_label = tk.Label(self.root)
        self.video_label.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            height=500,
            width=500,
        )

        self.cap = cv2.VideoCapture(0)

        # -----------------------------
        # FRAME - DATUM I VRIJEME LABELS
        # -----------------------------

        self.glavni_prikaz_label_datum_vrijeme = tk.Label(
            self.root,
            text="Ucitavanje...",
            font=FONT_STANDARD,
            bd=1,
            fg="white",
            bg="black",
            padx=5,
            pady=5,
            justify="center",
        )

        self.glavni_prikaz_label_datum_vrijeme.place(
            relx=0.025, rely=0.025, anchor="nw"
        )

        # -----------------------------
        # FRAME - TEMPERATURA LABELS
        # -----------------------------

        self.glavni_prikaz_label_temperatura = tk.Label(
            self.root,
            text="Ucitavanje...",
            font=FONT_STANDARD,
            bd=1,
            fg="white",
            bg="black",
            padx=5,
            pady=5,
            justify="center",
        )

        self.glavni_prikaz_label_temperatura.place(relx=0.975, rely=0.025, anchor="ne")

        # -----------------------------
        # UNUTARNJA TEMPERATURA
        # -----------------------------

        # -----------------------------
        #  DODATNE METRIKE
        # -----------------------------

        if DodatneMetrike.vlaznost_var:
            self.glavni_prikaz_label_vlaznost = tk.Label(
                self.root,
                text="Ucitavanje...",
                font=FONT_STANDARD,
                bd=1,
                fg="white",
                bg="black",
                padx=5,
                pady=5,
                justify="center",
            )

            self.glavni_prikaz_label_vlaznost.place(relx=0.975, rely=0.45, anchor="e")

        # -----------------------------
        # DODATI ISTO KAO GORE, ALI ZA TLAK
        # -----------------------------

        # ----------------------------
        # VRATI SE U POSTAVKE
        # ----------------------------
        self.back_to_main_screen_button = ttk.Button(self.root, text="Postavke")
        self.back_to_main_screen_button.place(relx=0.025, rely=0.95, anchor="w")

        # --------------------------
        # UPDATE-AJ NOVE PODATKE
        # --------------------------
        self.update_frame()

        self.root.after(1000, self.update_time_glavniPrikaz)
        self.root.after(1000, self.update_out_temp_glavniPrikaz)

        # --------------------------
        # Dodaj refresh podataka iz raspberrya
        # --------------------------

    # -----------------------------
    # FUNKCIJE
    # -----------------------------

    # =================================================
    # TODO: Ove dvije funkcije imamo i kod mainScreena
    # Imamo ponavljanje koje moramo izbjeci
    # To mozemo uciniti dajuci funkciji 3 argumenta (root, label, funkcija(funkcija prima samu sebe kao argument))
    # ================================================

    def update_time_glavniPrikaz(self):
        trenutno_vrijeme = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.glavni_prikaz_label_datum_vrijeme.config(text=f"{trenutno_vrijeme}")
        self.root.after(1000, self.update_time_glavniPrikaz)

    def update_out_temp_glavniPrikaz(self, grad="Zagreb"):
        Api_Key = "2606f769271b8d545fe3458b2b72ed9f"
        final_URL = f"http://api.openweathermap.org/data/2.5/weather?q={grad}&appid={Api_Key}&units=metric"
        try:
            response = requests.get(final_URL)
            response.raise_for_status()
            data = response.json()
            temperature = data["main"]["temp"]
            lokacija_display = grad
            self.glavni_prikaz_label_temperatura.configure(
                text=f"Temperatura u mjestu {lokacija_display}: {temperature}°C"
            )
        except requests.exceptions.RequestException as e:
            self.glavni_prikaz_label_temperatura.configure(text=f"Greska: {e}")
        self.root.after(5000, self.update_out_temp_glavniPrikaz)

    # ===================================
    # ===================================

    def update_frame(self) -> None:
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            img = Image.fromarray(frame)
            self.imgtk = ImageTk.PhotoImage(image=img)

            self.video_label.imgtk = self.imgtk
            self.video_label.configure(image=self.imgtk)

        self.video_label.after(10, self.update_frame)

    # ------------------------------
    # SenseHat mjerenja
    # ------------------------------
    # TODO: Import SenseHat i napraviti ova mjerenja

    def izmjeri_vlaznost(self) -> str:
        pass

    def izmjeri_tlak(self) -> str:
        pass

    def izmjeri_unutarnju_temperaturu(self) -> str:
        pass

    # -----------------------------
    # Funkcija koja provjerava dal je Kamera.kamera_var == True ili trenutno vrijeme spada u Kamera.kamera_hour
    # -----------------------------

    # -----------------------------
    # Funkcija koja nas ponovo vraca na MainMenuScreen
    # -----------------------------

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()
