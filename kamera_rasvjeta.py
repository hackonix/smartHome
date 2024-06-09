import tkinter as tk
from tkinter import ttk
import requests
from datetime import datetime

# Funkcija za dohvaćanje vremena zalaska sunca za Zagreb
def zalazak_sunca():
    response = requests.get(f'https://hr.meteocast.net/sunrise-sunset/hr/zagreb/#google_vignette')

# Glavni prozor
root = tk.Tk()
root.title("Smart Home Sustav")
root.geometry("600x500")

# Funkcija za prikaz postavki rasvjete u okviru
def postavke_rasvjeta():
    rasvjeta_postavke = tk.Frame(root, borderwidth=2, relief='groove')
    rasvjeta_postavke.place(x=200, y=50, width=300, height=200)  # Postavljanje okvira unutar glavnog prozora
    
    # Checkbox za automatsko paljenje po zalasku sunca
    sunset_var = tk.BooleanVar()
    tk.Checkbutton(rasvjeta_postavke, text="Automatski upali po zalasku sunca", variable=sunset_var).pack(pady=10)
    
    # Oznaka i unos za sat kad će se svjetlo upaliti
    tk.Label(rasvjeta_postavke, text="Upali svjetlo u (HH:MM):").pack(pady=10)
    
    hour_var = tk.StringVar()
    hour_entry = ttk.Entry(rasvjeta_postavke, textvariable=hour_var)
    hour_entry.pack(pady=5)
    
    def spremanje_postavki():
        if sunset_var.get():
            vrijeme_zalaska = zalazak_sunca()
            if vrijeme_zalaska:
                print(f"Svjetlo će se automatski upaliti po zalasku sunca u: {vrijeme_zalaska}")
            
        else:
            hour = hour_var.get()
            print(f"Svjetlo će se upaliti u: {hour} sati")
        rasvjeta_postavke.destroy()
    
    save_button = ttk.Button(rasvjeta_postavke, text="Spremi", command=spremanje_postavki)
    save_button.pack(pady=20)

# Gumb za otvaranje postavki rasvjete
light_button = ttk.Button(root, text="Rasvjeta", command=postavke_rasvjeta)
light_button.place(x=10, y=10, width=150, height=50)

# funkcija za prikaz postavke kamere
def postavke_kamere():
    kamera_postavke = tk.Frame(root, borderwidth=2, relief='groove')
    kamera_postavke.place(x=200, y=50, width=300, height=200) 

    tk.Checkbutton(kamera_postavke, text="Upaliti kameru pri zvonjavi").pack(padx=10)
    tk.Checkbutton(kamera_postavke, text="Nemoj upaliti kameru pri zvonjavi").pack(padx=10)

    def spremanje_odabira():
        print("Odabir spremljen!")
        kamera_postavke.destroy()

    ttk.Button(kamera_postavke, text="Spremi", command=spremanje_odabira).pack(padx=20, pady=10)
    
        
# Gumb za otvaranje postavki kamere
kamera_button = ttk.Button(root, text="Kamera", command=postavke_kamere)
kamera_button.place(y=10, x=180, width=150, height=50) 


root.mainloop()