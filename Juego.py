import tkinter as tk
from tkinter import messagebox
import threading as th
import time
import random

class Juego:
    def subir(self, event):
        if self.y > -250:
            self.y -= 20

    def bajar(self, event):
        if self.y < 250:
            self.y += 20

    def iniciarJuego(self, *args):
        self.btnIniciar.config(state="disabled")
        hilo = th.Thread(target=self.lanzarTuberias)
        hilo.start()
        self.mover_jugador()

    def mover_jugador(self):
        self.lienzo.delete("jugador")
        self.dibujar_pajaro()
        self.ventana.after(20, self.mover_jugador)

    def lanzarTuberias(self):
        try:
            while True:
                espacio = 150
                altura_superior = random.randint(100, 300)
                altura_inferior = 600 - altura_superior - espacio
                x = 800
                ancho = 60

                tubo_sup = self.lienzo.create_rectangle(x, 0, x + ancho, altura_superior, fill="green", tags="tubo")
                tubo_inf = self.lienzo.create_rectangle(x, 600 - altura_inferior, x + ancho, 600, fill="green", tags="tubo")

                while x + ancho > 0:
                    self.lienzo.move(tubo_sup, -5, 0)
                    self.lienzo.move(tubo_inf, -5, 0)
                    x -= 5

                    if self.colision(tubo_sup) or self.colision(tubo_inf):
                        messagebox.showinfo("Fin del juego", f"¡Perdiste! Puntaje: {self.puntaje}")
                        self.ventana.destroy()
                        return

                    time.sleep(self.velocidad)

                self.puntaje += 1
                self.lblPuntaje.config(text="Puntaje = " + str(self.puntaje))
                if self.puntaje % 5 == 0 and self.velocidad > 0.004:
                    self.velocidad -= 0.001

                self.lienzo.delete(tubo_sup)
                self.lienzo.delete(tubo_inf)
        except Exception as e:
            print("Error en lanzarTuberias:", e)

    def colision(self, obstaculo_id):
        jugador_coords = self.lienzo.bbox("jugador")
        obstaculo_coords = self.lienzo.coords(obstaculo_id)

        if not jugador_coords or not obstaculo_coords:
            return False

        jx1, jy1, jx2, jy2 = jugador_coords
        ox1, oy1, ox2, oy2 = obstaculo_coords

        return not (jx2 < ox1 or jx1 > ox2 or jy2 < oy1 or jy1 > oy2)

    def dibujar_pajaro(self):
        x = 60
        y = 300 + self.y

        self.lienzo.create_oval(x-15, y-15, x+15, y+15, fill="yellow", outline="black", width=2, tags="jugador")
        self.lienzo.create_polygon(x+15, y, x+25, y-5, x+25, y+5, fill="red", outline="black", tags="jugador")
        self.lienzo.create_oval(x+5, y-10, x+10, y-5, fill="white", outline="black", tags="jugador")
        self.lienzo.create_oval(x+7, y-8, x+9, y-6, fill="black", tags="jugador")

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Flappy Bird Geométrico")
        self.ventana.config(width=800, height=600)
        self.ventana.resizable(0, 0)

        self.y = 0
        self.puntaje = 0
        self.velocidad = 0.016  # segundos entre frames

        self.lienzo = tk.Canvas(self.ventana, width=800, height=600, bg="skyblue")
        self.lienzo.place(x=0, y=0)

        self.lblPuntaje = tk.Label(self.lienzo, text="Puntaje = 0", font=("Arial", 14), bg="skyblue")
        self.lblPuntaje.place(relx=0.5, y=30, anchor="center")

        self.btnIniciar = tk.Button(self.lienzo, text="Iniciar Juego", font=("Arial", 12))
        self.btnIniciar.place(relx=0.5, rely=0.95, anchor="center")
        self.btnIniciar.bind("<Button-1>", self.iniciarJuego)

        # ✅ Teclas permitidas: Flechas y W/S en mayúscula y minúscula
        self.ventana.bind("<Up>", self.subir)
        self.ventana.bind("<Down>", self.bajar)
        self.ventana.bind("w", self.subir)
        self.ventana.bind("s", self.bajar)
        self.ventana.bind("W", self.subir)
        self.ventana.bind("S", self.bajar)

        self.dibujar_pajaro()

        self.ventana.mainloop()

