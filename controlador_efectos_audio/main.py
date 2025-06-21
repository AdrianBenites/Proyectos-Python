import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pygame
import os

# Inicializar pygame mixer
pygame.mixer.init()

# Ruta donde están los sonidos e íconos
SOUNDS_DIR = "static/sounds"
ICONS_DIR = "static/icons"

# Diccionario de sonidos de ejemplo
SONIDOS = {
    "Aplausos": ("applause.wav", "applause.gif"),
    "Campana": ("bell.wav", "bell.gif"),
    "Trompeta": ("trumpet.wav", "trumpet.gif"),
    "Bocina": ("horn.wav", "horn.gif"),
    "Risa": ("laugh.wav", "laugh.gif"),
    "Suspenso": ("suspense.wav", "suspense.gif"),
    "Error": ("error.wav", "error.gif")
}

class PanelAudio(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🎧 Panel de Efectos de Audio")
        self.configure(bg="#1e1e1e")
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TButton", background="#333", foreground="#fff", font=("Segoe UI", 10), padding=10)
        self.crear_botones()

    def crear_botones(self):
        fila = 0
        columna = 0
        for nombre, (archivo_sonido, icono) in SONIDOS.items():
            ruta_sonido = os.path.join(SOUNDS_DIR, archivo_sonido)
            ruta_icono = os.path.join(ICONS_DIR, icono)

            if os.path.exists(ruta_icono):
                imagen = Image.open(ruta_icono)
                imagen = imagen.resize((64, 64))
                icono_img = ImageTk.PhotoImage(imagen)
            else:
                icono_img = None

            btn = ttk.Button(self, text=nombre, image=icono_img, compound="top", command=lambda s=ruta_sonido: self.reproducir_sonido(s))
            btn.image = icono_img
            btn.grid(row=fila, column=columna, padx=10, pady=10)

            columna += 1
            if columna > 2:
                fila += 1
                columna = 0

    def reproducir_sonido(self, ruta):
        try:
            pygame.mixer.music.load(ruta)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Error al reproducir sonido: {e}")

if __name__ == "__main__":
    app = PanelAudio()
    app.mainloop()
