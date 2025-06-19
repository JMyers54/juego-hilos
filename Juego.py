import tkinter as tk
from tkinter import messagebox
import threading as th
import time
import random

class Juego():
    def subir(self, event):
        if self.lienzo.coords("jugador")[1] >= 10:
            self.y -= 10
            self.paint()

    def bajar(self, event):
        if self.lienzo.coords("jugador")[3] <= 590:
            self.y += 10
            self.paint()

    def iniciarJuego(self, *args):
        hilo = th.Thread(target=self.lanzarObstaculos)
        hilo.start()

    def lanzarObstaculos(self):
        while True:
            y_pos = random.randint(0, 500)  # altura inicial aleatoria
            altura = random.randint(80, 200)  # altura del obstáculo
            color = random.choice(self.colores)

            # Crear obstáculo más grande
            obstaculo = self.lienzo.create_rectangle(
                800, y_pos, 830, y_pos + altura, fill=color, tags="obstaculo"
            )

            while self.lienzo.coords(obstaculo)[2] > 0:
                coords = self.lienzo.coords(obstaculo)
                self.lienzo.move(obstaculo, -5, 0)

                # Verificar colisión
                if self.detectar_colision(self.lienzo.coords("jugador"), coords):
                    messagebox.showinfo("Fin del juego", "¡Perdiste! Puntaje: " + str(self.puntaje))
                    self.ventana.destroy()
                    return

                time.sleep(self.velocidad)

            self.lienzo.delete(obstaculo)
            self.puntaje += 1
            self.lblPuntaje.config(text="Puntaje = " + str(self.puntaje))

            # Aumentar dificultad
            if self.puntaje % 5 == 0 and self.velocidad > 0.005:
                self.velocidad -= 0.001

    def detectar_colision(self, jugador, obstaculo):
        return not (
            jugador[2] < obstaculo[0] or
            jugador[0] > obstaculo[2] or
            jugador[3] < obstaculo[1] or
            jugador[1] > obstaculo[3]
        )

    def paint(self):
        self.lienzo.delete("jugador")
        self.lienzo.create_oval(5, 275 + self.y, 55, 325 + self.y, fill="blue", tags="jugador")

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Juego de esquivar obstáculos grandes")
        self.ventana.config(width=800, height=600)
        self.ventana.resizable(0, 0)

        self.x = 0
        self.y = 0
        self.puntaje = 0
        self.velocidad = 0.016  # 60 FPS aprox
        self.colores = ["red", "green", "black", "yellow", "pink"]

        self.lienzo = tk.Canvas(self.ventana, width=800, height=600)
        self.lienzo.place(x=0, y=0)

        self.lblPuntaje = tk.Label(self.lienzo, text="Puntaje = 0")
        self.lblPuntaje.place(relx=0.5, y=30, anchor="center")

        self.btnIniciar = tk.Button(self.lienzo, text="Iniciar Juego")
        self.btnIniciar.place(relx=0.5, rely=0.95, anchor="center")
        self.btnIniciar.bind("<Button-1>", self.iniciarJuego)

        self.ventana.bind("<Up>", self.subir)
        self.ventana.bind("<Down>", self.bajar)

        self.paint()

        self.ventana.mainloop()
