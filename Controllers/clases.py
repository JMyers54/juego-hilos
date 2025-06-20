from tkinter import *
import tkinter as tk
from tkinter import messagebox
from Models.ConexionBD import ConexionDB


class Usuario():
    def __init__(self, nombre, contraseña, email):
        self.nombre = nombre
        self.contraseña = contraseña
        self.email = email
        
    def registrar_usuario(self):
        db = ConexionDB()
        try:
            db.cursor.execute("INSERT INTO usuarios(NOMBRE, Contraseña, Email) VALUES (%s,%s,%s)",(self.contraseña, self.nombre, self.email))
            db.conn.commit()
        finally:
            db.cerrar()