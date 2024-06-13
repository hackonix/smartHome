import tkinter as tk
import requests
import cv2
from typing import Optional
from tkinter import ttk
from datetime import datetime
from PIL import Image, ImageTk
from sense_emu import SenseHat


# sense = SenseHat()
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
KALENDAR_PLACEHOLDER = "KALENDAR"

ZELJENI_EVENT = "<Button-1>"


class MainMenu:
    def __init__(self, root: tk.Tk, screen_size: str = "800x600") -> None:
        self.root = root
        self.root.title = "SmartHome"
        self.root.geometry(screen_size)

        self.lokacija = "Zagreb"

        # -----------------------------
        # PRIKAZ DATUMA
        # -----------------------------
        self.label_datum = tk.Label(self.root, text="Datum, loading...")
        self.label_datum.place(relx=0.025, rely=0.05, anchor="w")
        # TODO: Napraviti funkciju koja update-a self.label_datum

        # -----------------------------
        # PRIKAZ VANJESKE TEMPERATURE
        # -----------------------------
        self.label_vanjska_temp = tk.Label(
            self.root, text="Vanjska temperatura, loading..."
        )
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

        # Kalendar button
        self.button_kalendar = tk.Button(self.root, text=KALENDAR_PLACEHOLDER)
        self.button_kalendar.place(
            relx=0.35,
            rely=0.375,
            height=BUTTON_HEIGHT,
            width=235,
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

        self.button_kalendar.bind(
            ZELJENI_EVENT,
            self.button_kalendar_on_click,
        )

        # -------------------------------
        # INICIJALIZACIJA OBJEKATA
        # -------------------------------
        self.rasvjeta_screen: Optional[RasvjetaScreen] = None
        self.temperatura_screen: Optional[TemperaturaScreen] = None
        self.kamera_screen: Optional[RasvjetaScreen] = None
        self.dodatne_metrike_screen: Optional[DodatneMetrikeScreen] = None
        self.kalendar_screen: Optional[KalendarScreen] = None

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
        self.rasvjeta_screen = RasvjetaScreen(self.root)

    def button_temp_on_click(self, event):
        self.temperatura_screen = TemperaturaScreen(self.root)

    def button_kamera_on_click(self, event):
        self.kamera_screen = KameraScreen(self.root)

    def button_dodatne_metrike_on_click(self, event):
        self.dodatne_metrike_screen = DodatneMetrikeScreen(self.root)

    def button_kalendar_on_click(self, event):
        self.kalendar_screen = KalendarScreen(self.root)

    def button_glavni_prikaz_on_click(self, event):
        self.glavni_prikaz_screen = GlavniPrikazScreen(
            self.root,
            self.rasvjeta_screen,
            self.temperatura_screen,
            self.kamera_screen,
            self.dodatne_metrike_screen,
            self.kalendar_screen,
        )


class RasvjetaScreen(MainMenu):
    def __init__(
        self,
        root: tk.Tk,
        screen_size: str = "800x600",
    ) -> None:
        super().__init__(root, screen_size)

        self.title = "Postavke rasvjete"

        self.rasvjeta_postavke = tk.Frame(self.root, borderwidth=2, relief="groove")

        self.rasvjeta_postavke.place(
            relx=0.315,
            rely=0.2,
            width=300,
            height=200,
        )  # Postavljanje okvira unutar glavnog prozora

        self.sunset_var = tk.BooleanVar()

        tk.Checkbutton(
            self.rasvjeta_postavke,
            text="Upali svjetlo",
            variable=self.sunset_var,
        ).pack(pady=10)

        # Oznaka i unos za sat kad će se svjetlo upaliti
        tk.Label(
            self.rasvjeta_postavke, text="Upali/iskljuci svjetlo u (HH:MM) - (HH:MM):"
        ).pack(pady=10)

        self.hour_var = tk.StringVar()
        self.hour_entry = ttk.Entry(self.rasvjeta_postavke)
        self.hour_entry.pack(pady=5)

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
            self.rasvjeta_upaljena = self.sunset_var.get()
            self.hour_var = "00:00 - 23:59"

        else:
            self.rasvjeta_upaljena = False
            self.hour_var = self.hour_entry.get()
        self.rasvjeta_postavke.destroy()

    def zalazak_sunca(self):
        response = requests.get(
            f"https://hr.meteocast.net/sunrise-sunset/hr/zagreb/#google_vignette"
        )

        return response


class TemperaturaScreen(MainMenu):
    def __init__(
        self,
        root: tk.Tk,
        screen_size: str = "800x600",
    ) -> None:
        super().__init__(root, screen_size)

        self.title = "Temperatura - Postavke"

        self.temperatura_postavke = tk.Frame(self.root, borderwidth=2, relief="groove")

        self.temperatura_postavke.place(relx=0.315,
            rely=0.2,
            width=300,
            height=200,)

        # Oznaka i unos temperature
        tk.Label(self.temperatura_postavke, text="Zeljena temperatura:").pack(pady=10)

        self.zeljena_temperatura = tk.StringVar()
        self.zeljena_temperatura_entry = ttk.Entry(self.temperatura_postavke)
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
    def __init__(self, root: tk.Tk, screen_size: str = "800x600") -> None:
        super().__init__(root, screen_size)

        self.title = "Kamera - Postavke"

        self.kamera_postavke = tk.Frame(self.root, borderwidth=2, relief="groove")

        self.kamera_postavke.place(
            relx=0.315,
            rely=0.2,
            width=300,
            height=200,
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
            self.kamera_postavke,
            text="Upali/iskljuci kameru u (HH:MM) - (HH:MM):",
        ).pack(pady=10)

        self.kamera_hour = tk.StringVar()

        self.kamera_hour_entry = ttk.Entry(
            self.kamera_postavke,
            textvariable=self.kamera_hour,
        )
        self.kamera_hour_entry.pack(pady=5)

        self.kamera_save_button = ttk.Button(
            self.kamera_postavke,
            text="Spremi",
            command=self.spremanje_postavki_kamere,
        )

        self.kamera_save_button.pack(pady=20)

    # -----------------------------
    # KameraScreen FUNKCIJE
    # -----------------------------
    def spremanje_postavki_kamere(self):
        if self.kamera_var.get():
            self.kamera_hour = "00:00 - 23:59"
        else:
            self.kamera_hour = self.kamera_hour.get()

        self.kamera_postavke.destroy()


class DodatneMetrikeScreen(MainMenu):
    def __init__(self, root: tk.Tk, screen_size: str = "800x600") -> None:
        super().__init__(root, screen_size)

        self.title = "Doodatne metrike - postavke"

        self.dodatne_metrike_postavke = tk.Frame(
            self.root,
            borderwidth=2,
            relief="groove",
        )

        self.dodatne_metrike_postavke.place(
            relx=0.315,
            rely=0.2,
            width=300,
            height=200,
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

    # ---------------------------
    # DodatneMetrikeScreen FUNKCIJE
    # ---------------------------
    def spremanje_postavki_dodatne_metrike(self):
        if self.vlaznost_var.get():
            self.vlaznost_var = self.vlaznost_var.get()

        if self.tlak_var.get():
            self.tlak_var = self.tlak_var.get()

        self.dodatne_metrike_postavke.destroy()


class KalendarScreen(MainMenu):
    def __init__(self, root: tk.Tk, screen_size: str = "800x600") -> None:
        super().__init__(root, screen_size)

        self.title = "Kalendar - postavke"

        self.kalendar_postavke = tk.Frame(self.root, borderwidth=2, relief="groove")

        self.kalendar_postavke.place(
            relx=0.315,
            rely=0.2,
            width=300,
            height=200,
        )  # Postavljanje okvira unutar glavnog prozora

        tk.Label(self.kalendar_postavke, text="Napravi novi unos u kalendar").pack(
            pady=10
        )

        # Inicijalizacija liste u koju cemo spremati aktivnosti za kalendar
        self.kalendar_lista_aktivnosti = []
        self.kalendar_entry = ttk.Entry(self.kalendar_postavke)
        self.kalendar_entry.pack(pady=5)

        kalendar_save_button = ttk.Button(
            self.kalendar_postavke,
            text="Spremi",
            command=self.spremanje_postavki_kalendara,
        )
        kalendar_save_button.pack(pady=5)

        kalendar_exit_button = ttk.Button(
            self.kalendar_postavke,
            text="Zatvori",
            command=self.zatvori_postavke_kalendara,
        )
        kalendar_exit_button.pack(pady=5)

        # -----------------------------
        # KalendarScreen FUNKCIJE
        # -----------------------------

    def spremanje_postavki_kalendara(self):
        if self.kalendar_entry.get():
            self.kalendar_lista_aktivnosti.append(self.kalendar_entry.get())
            self.kalendar_entry.delete(0, tk.END)
        

    def zatvori_postavke_kalendara(self):
        self.kalendar_postavke.destroy()


class GlavniPrikazScreen(
    RasvjetaScreen, TemperaturaScreen, KameraScreen, DodatneMetrikeScreen, MainMenu
):
    def __init__(
        self,
        root: tk.Tk,
        rasvjeta_screen,
        temperatura_screen,
        kamera_screen,
        dodatne_metrike_screen,
        kalendar_screen,
        screen_size: str = "800x600",
    ) -> None:
        super().__init__(root, screen_size)
        self.title = "Glavni prikaz"
        self.root = root

        self.glavni_prikaz_frame = tk.Frame(self.root)
        self.glavni_prikaz_frame.pack(fill="both", expand=True)

        self.rasvjeta_screen = rasvjeta_screen
        self.temperatura_screen = temperatura_screen
        self.kamera_screen = kamera_screen
        self.dodatne_metrike_screen = dodatne_metrike_screen
        self.kalendar_screen = kalendar_screen

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # -----------------------------
        # RASVJETA LABEL
        # -----------------------------

        self.rasvjeta_label = tk.Label(
            self.glavni_prikaz_frame, foreground="black", bg="black", width=10, height=5
        )
        self.rasvjeta_label.place(relx=0.05, rely=0.25)

        # -----------------------------
        # VIDEO FRAME PLACEHOLDER
        # -----------------------------

        self.video_label = ttk.Label(self.glavni_prikaz_frame)
        self.video_label.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            height=500,
            width=500,
        )
        self.cap = cv2.VideoCapture(0)

        # -----------------------------
        # TRENUTNI DATUM I VRIJEME
        # -----------------------------

        self.glavni_prikaz_label_datum_vrijeme = ttk.Label(
            self.glavni_prikaz_frame,
            text="Ucitavanje...",
            font=FONT_STANDARD,
            justify="center",
        )

        self.glavni_prikaz_label_datum_vrijeme.place(
            relx=0.025, rely=0.025, anchor="nw"
        )

        # -----------------------------
        # VANJSKA TEMPERATURA
        # -----------------------------

        self.glavni_prikaz_label_temperatura = ttk.Label(
            self.glavni_prikaz_frame,
            text="Ucitavanje...",
            font=FONT_STANDARD,
            justify="center",
        )

        self.glavni_prikaz_label_temperatura.place(relx=0.975, rely=0.025, anchor="ne")

        # -----------------------------
        # UNUTARNJA TEMPERATURA #TODO: DODAJ FUNKCIONALNOST
        # -----------------------------
        self.unutarnja_temperatura_label = ttk.Label(
            self.glavni_prikaz_frame,
            text="Ucitavanje...",
            font=FONT_STANDARD,
            justify="center",
        )

        self.unutarnja_temperatura_label.place(relx=0.975, rely=0.075, anchor="ne")

        # -----------------------------
        #  DODATNE METRIKE
        # -----------------------------

        if self.dodatne_metrike_screen.vlaznost_var == True:
            self.glavni_prikaz_label_vlaznost = ttk.Label(
                self.glavni_prikaz_frame,
                text="Ucitavanje...",
                font=FONT_STANDARD,
                justify="center",
            )

            self.glavni_prikaz_label_vlaznost.place(relx=0.975, rely=0.45, anchor="e")

        if self.dodatne_metrike_screen.tlak_var == True:
            self.glavni_prikaz_label_tlak = ttk.Label(
                self.glavni_prikaz_frame,
                text="Ucitavanje...",
                font=FONT_STANDARD,
                justify="center",
            )

            self.glavni_prikaz_label_tlak.place(relx=0.975, rely=0.75, anchor="e")

        # -----------------------------
        #  KALENDAR
        # -----------------------------
        if self.kalendar_screen.kalendar_lista_aktivnosti:
            self.kalendar_label = ttk.Label(
                self.glavni_prikaz_frame,
                text="Ucitavanje kalendara",
                font=FONT_STANDARD,
                justify="center",
            )
            self.kalendar_label.place(relx=0.5, rely=0.95)

        # ----------------------------
        # VRATI SE U POSTAVKE - BUTTON
        # ----------------------------
        self.vrati_se_u_postavke_button = ttk.Button(
            self.root, text="Postavke"
        )
        self.vrati_se_u_postavke_button.place(relx=0.025, rely=0.95, anchor="w")
        

        # --------------------------
        # UPDATE-AJ PODATKE
        # --------------------------

        # RASVJETA
        if (
            self.rasvjeta_screen.rasvjeta_upaljena == True
            or self.vrijeme_je_u_zadanom_opsegu(self.rasvjeta_screen.hour_var)
        ):
            self.root.after(6000, self.update_rasvjeta_label)
        else:
            self.rasvjeta_label.configure(bg="black")

        # KAMERA
        if self.kamera_screen.kamera_var == True or self.vrijeme_je_u_zadanom_opsegu(
            self.kamera_screen.kamera_hour
        ):
            self.update_frame()

        # DATUM I VRIJEME
        self.glavni_prikaz_frame.after(5000, self.update_time_glavniPrikaz)

        # VANJSKA TEMPERATURA
        self.glavni_prikaz_frame.after(5500, self.update_out_temp_glavniPrikaz)

        # KALENDAR
        self.glavni_prikaz_frame.after(6500, self.update_kalendar_label)

        # --------------------------
        # Update Raspberry data
        # --------------------------
        # self.root.after(1000, self.dohvati_unutarnju_temperaturu)
        # self.root.after(1000, self.dohvati_vlaznost)
        # self.root.after(1000, self.dohvati_tlak)

        # --------------------------
        # POVRATAK U MAIN SCREEN
        # --------------------------
        self.vrati_se_u_postavke_button.bind(ZELJENI_EVENT, self.postavke_on_click)

    # -----------------------------
    # FUNKCIJE
    # -----------------------------

    # =================================================
    # TODO: Ove dvije funkcije imamo i kod mainScreena
    # Imamo ponavljanje koje moramo izbjeci
    # To mozemo uciniti dajuci funkciji 3 argumenta (root, label, funkcija(funkcija prima samu sebe kao argument))
    # ================================================
    def update_kalendar_label(self):
        if self.kalendar_screen.kalendar_lista_aktivnosti:
            for aktivnost in self.kalendar_screen.kalendar_lista_aktivnosti:
                self.kalendar_label.configure(text=aktivnost)
                self.root.after(3000, self.update_kalendar_label)

    def update_rasvjeta_label(self):
        self.rasvjeta_label.configure(bg="yellow")
        self.root.after(5000, self.update_rasvjeta_label)

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

        self.video_label.after(100, self.update_frame)

    # ------------------------------
    # SenseHat mjerenja
    # ------------------------------

    def dohvati_vlaznost(self) -> str:
        vlaznost = sense.get_humidity()
        self.glavni_prikaz_label_vlaznost.config(text=f"Vlaznost iznosi: {vlaznost} %")
        self.root.after(5000, self.dohvati_vlaznost)

    def dohvati_tlak(self) -> str:
        tlak = sense.get_pressure()
        self.glavni_prikaz_label_tlak.config(text=f"Tlak iznosi: {tlak} hPa")
        self.root.after(5000, self.dohvati_tlak)

    def dohvati_unutarnju_temperaturu(self) -> str:
        temperatura = sense.get_temperature()
        self.unutarnja_temperatura_label.config(
            text=f"Temperatura iznosi {temperatura:.2f} stupnjeva"
        )
        self.root.after(5000, self.dohvati_unutarnju_temperaturu)

    # -----------------------------
    # Funkcija koja provjerava dal je Kamera.kamera_var == True ili trenutno vrijeme spada u Kamera.kamera_hour
    # -----------------------------
    def vrijeme_je_u_zadanom_opsegu(self, vremenski_opseg):
        pocetno_vrijeme_str, zavrsno_vrijeme_str = vremenski_opseg.split(" - ")

        pocetno_vrijeme = datetime.strptime(pocetno_vrijeme_str, "%H:%M").time()
        zavrsno_vrijeme = datetime.strptime(zavrsno_vrijeme_str, "%H:%M").time()

        trenutno_vrijeme = datetime.now().time()

        if pocetno_vrijeme < zavrsno_vrijeme:
            return pocetno_vrijeme <= trenutno_vrijeme <= zavrsno_vrijeme
        else:
            return (
                trenutno_vrijeme >= pocetno_vrijeme
                or trenutno_vrijeme <= zavrsno_vrijeme
            )

    # -----------------------------
    # Funkcija koja nas ponovo vraca na MainMenuScreen
    # -----------------------------
    def postavke_on_click(self, event):
        self.glavni_prikaz_frame.destroy()
        MainMenu(self.root)

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()
