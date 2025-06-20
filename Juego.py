import tkinter as tk
from tkinter import messagebox
import threading as th
import time
import random
from PIL import Image, ImageTk
import pygame.mixer as mixer

class Juego:
    def subir(self, event):
        if self.y > -250:
            self.y -= 20

    def bajar(self, event):
        if self.y < 250:
            self.y += 20

    def iniciarJuego(self, *args):
        if self.juego_activo:
            return
        self.juego_activo = True
        self.btnIniciar.config(state="disabled")
        self.x = 0
        hilo = th.Thread(target=self.lanzarTuberias)
        hilo.start()
        self.mover_jugador()

    def mover_jugador(self):
        if not self.juego_activo:
            return
        self.lienzo.delete("jugador")
        self.dibujar_pez()
        self.ventana.after(20, self.mover_jugador)

    def lanzarTuberias(self):
        try:
            while self.juego_activo:
                obstaculos = self.crear_obstaculo()
                x = 800
                ancho = 60

                while x + ancho > 0 and self.juego_activo:
                    for obs in obstaculos:
                        self.lienzo.move(obs, -5, 0)
                        if self.colision(obs):
                            self.sonido_choque.play()  # Sonido al chocar
                            self.guardar_puntaje()
                            messagebox.showinfo("Fin del juego", f"¡Perdiste! Puntaje: {self.puntaje}")
                            self.fin_del_juego()
                            return
                    x -= 5
                    time.sleep(self.velocidad)

                if self.juego_activo:
                    self.puntaje += 1
                    self.lblPuntaje.config(text="Puntaje = " + str(self.puntaje))
                    self.sonido_paso.play()  # Sonido al pasar el tubo
                    if self.puntaje % 3 == 0 and self.velocidad > 0.004:
                        self.velocidad -= 0.002

                for obs in obstaculos:
                    self.lienzo.delete(obs)

        except Exception as e:
            print("Error en lanzarTuberias:", e)

    def crear_obstaculo(self):
        espacio = 100
        altura_superior = random.randint(100, 300)
        altura_inferior = 600 - altura_superior - espacio
        x = 800
        ancho = 60
        tubo_sup = self.lienzo.create_rectangle(x, 0, x + ancho, altura_superior, fill="green", tags="tubo")
        tubo_inf = self.lienzo.create_rectangle(x, 600 - altura_inferior, x + ancho, 600, fill="green", tags="tubo")
        return [tubo_sup, tubo_inf]

    def fin_del_juego(self):
        self.juego_activo = False
        self.btnIniciar.config(state="normal")
        self.puntaje = 0
        self.velocidad = 0.016
        self.x = 0
        self.y = 0
        self.lblPuntaje.config(text="Puntaje = 0")
        self.lienzo.delete("tubo")

    def colision(self, obstaculo_id):
        jugador_coords = self.lienzo.bbox("jugador")
        obstaculo_coords = self.lienzo.coords(obstaculo_id)

        if not jugador_coords or not obstaculo_coords:
            return False

        jx1, jy1, jx2, jy2 = jugador_coords
        ox1, oy1, ox2, oy2 = obstaculo_coords

        margen = 20  # reduce la hitbox
        jx1 += margen
        jy1 += margen
        jx2 -= margen
        jy2 -= margen

        return not (jx2 < ox1 or jx1 > ox2 or jy2 < oy1 or jy1 > oy2)

    def dibujar_pez(self):
        x = 60
        y = 300 + self.y
        self.lienzo.create_image(x, y, image=self.pez_img, tags="jugador")

    def abrir_cuentas(self):
        ventana_cuentas = tk.Toplevel(self.ventana)
        ventana_cuentas.title("Cuentas")
        ventana_cuentas.geometry("250x150")

        tk.Label(ventana_cuentas, text="Bienvenido").pack(pady=10)

        btn_login = tk.Button(ventana_cuentas, text="Iniciar Sesión", command=self.ventana_login)
        btn_login.pack(pady=5)

        btn_registro = tk.Button(ventana_cuentas, text="Registrarse", command=self.ventana_registro)
        btn_registro.pack(pady=5)

    def ventana_login(self):
        win = tk.Toplevel(self.ventana)
        win.title("Iniciar Sesión")
        win.geometry("250x200")

        tk.Label(win, text="Usuario").pack()
        entry_usuario = tk.Entry(win)
        entry_usuario.pack()

        tk.Label(win, text="Contraseña").pack()
        entry_contra = tk.Entry(win, show="*")
        entry_contra.pack()

        def login():
            user = entry_usuario.get()
            contra = entry_contra.get()
            for jugador in self.jugadores:
                if jugador["usuario"] == user and jugador.get("contra") == contra:
                    self.usuario_actual = user
                    messagebox.showinfo("Login exitoso", f"Bienvenido {user}")
                    win.destroy()
                    return
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

        tk.Button(win, text="Entrar", command=login).pack(pady=10)

    def ventana_registro(self):
        win = tk.Toplevel(self.ventana)
        win.title("Registro")
        win.geometry("250x200")

        tk.Label(win, text="Nuevo usuario").pack()
        entry_usuario = tk.Entry(win)
        entry_usuario.pack()

        tk.Label(win, text="Contraseña").pack()
        entry_contra = tk.Entry(win, show="*")
        entry_contra.pack()

        def registrar():
            user = entry_usuario.get()
            contra = entry_contra.get()
            for jugador in self.jugadores:
                if jugador["usuario"] == user:
                    messagebox.showerror("Error", "Usuario ya existe")
                    return
            self.jugadores.append({"usuario": user, "contra": contra, "puntaje": 0})
            messagebox.showinfo("Registro exitoso", f"Usuario {user} creado")
            win.destroy()

        tk.Button(win, text="Registrar", command=registrar).pack(pady=10)

    def mostrar_puntajes(self):
        win = tk.Toplevel(self.ventana)
        win.title("Puntajes")
        win.geometry("300x300")

        tk.Label(win, text="Jugadores", font=("Arial", 12, "bold")).pack(pady=10)

        for jugador in self.jugadores:
            texto = f"{jugador['usuario']} - Puntaje: {jugador.get('puntaje', 0)}"
            tk.Label(win, text=texto).pack()

    def guardar_puntaje(self):
        for jugador in self.jugadores:
            if jugador["usuario"] == self.usuario_actual:
                jugador["puntaje"] = max(jugador.get("puntaje", 0), self.puntaje)

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Flappy Fish")
        self.ventana.config(width=800, height=600)
        self.ventana.resizable(0, 0)

        self.y = 0
        self.puntaje = 0
        self.velocidad = 0.016
        self.usuario_actual = "admin"
        self.juego_activo = False
        self.jugadores = [{"usuario": "admin", "contra": "123", "puntaje": 0}]

        # Inicializar sonidos
        mixer.init()
        self.sonido_paso = mixer.Sound("juego-hilos\sounds\WhatsApp Audio 2025-06-19 at 7.11.06 PM.mpeg")
        self.sonido_choque = mixer.Sound("juego-hilos\sounds\WhatsApp Audio 2025-06-19 at 7.14.14 PM.mpeg")

        self.lienzo = tk.Canvas(self.ventana, width=800, height=600)
        self.lienzo.place(x=0, y=0)

        fondo_img = Image.open(r"juego-hilos\icons\agua.png.png").resize((800, 600))
        self.fondo_img = ImageTk.PhotoImage(fondo_img)
        self.lienzo.create_image(0, 0, anchor="nw", image=self.fondo_img)

        pez = Image.open(r"juego-hilos\icons\a-single-fish-in-pixel-art-style-vector-removebg-preview.png").resize((100, 100))
        self.pez_img = ImageTk.PhotoImage(pez)

        self.lblPuntaje = tk.Label(self.lienzo, text="Puntaje = 0", font=("Arial", 14), bg="skyblue")
        self.lblPuntaje.place(relx=0.5, y=30, anchor="center")

        self.btnIniciar = tk.Button(self.lienzo, text="Iniciar Juego", font=("Arial", 12))
        self.btnIniciar.place(relx=0.5, rely=0.95, anchor="center")
        self.btnIniciar.bind("<Button-1>", self.iniciarJuego)

        self.btnCuentas = tk.Button(self.lienzo, text="CUENTAS", font=("Arial", 12), command=self.abrir_cuentas)
        self.btnCuentas.place(relx=0.35, rely=0.95, anchor="center")

        self.btnPuntajes = tk.Button(self.lienzo, text="PUNTAJES", font=("Arial", 12), command=self.mostrar_puntajes)
        self.btnPuntajes.place(relx=0.65, rely=0.95, anchor="center")

        self.ventana.bind("<Up>", self.subir)
        self.ventana.bind("<Down>", self.bajar)
        self.ventana.bind("w", self.subir)
        self.ventana.bind("s", self.bajar)
        self.ventana.bind("W", self.subir)
        self.ventana.bind("S", self.bajar)

        self.dibujar_pez()
        self.ventana.mainloop()