import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("kamera prozor")
root.geometry("600x500")

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
