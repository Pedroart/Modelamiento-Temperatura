import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tkinter as tk
from tkinter import ttk

class Bloque:
    def __init__(self, ancho, alto, masa, calorEspecifico):
        self.ancho = ancho
        self.alto = alto
        self.masa = masa
        self.calorEspecifico = calorEspecifico
        self.area = ancho * alto
        self.temperatura = 0

class Aire:
    def __init__(self, c, h):
        self.c = c
        self.h = h
        self.coeficientePelicula = 0
        self.temperatura = 0
        self.velocidadFlujo = 0
        self.densidad = 1.225  # kg/m³
        self.calorEspecifico = 1006  # J/kgK
        self.calcularh()

    def calcularh(self):
        self.coeficientePelicula = self.c * np.power(self.velocidadFlujo, 0.5)

class TransferenciaCalor:
    def __init__(self):
        self.bloque = Bloque(1, 1, 1, 900)
        self.aireIngreso = Aire(10, 0.65)
        self.aireSalida = Aire(10, 0.65)
        self.historial_tiempo = []
        self.historial_temp_bloque = []
        self.historial_temp_aire_salida = []

    def transferencia_conveccion_bloque(self):
        h = self.aireIngreso.coeficientePelicula
        Q = h * self.bloque.area * (self.bloque.temperatura - self.aireIngreso.temperatura)
        self.bloque.temperatura += -Q / (self.bloque.masa * self.bloque.calorEspecifico)
        dm = self.aireIngreso.densidad * self.aireIngreso.velocidadFlujo * self.bloque.area
        self.aireSalida.temperatura = self.aireIngreso.temperatura + Q / (dm * self.aireIngreso.calorEspecifico)

    def simulacion(self, tiempoSegundos, tempInitBloque, tempInitAire, velAire=100):
        self.bloque.temperatura = tempInitBloque
        self.aireIngreso.temperatura = tempInitAire
        self.aireIngreso.velocidadFlujo = velAire
        self.aireIngreso.calcularh()
        
        fig, ax = plt.subplots()
        ax.set_xlim(0, tiempoSegundos)
        ax.set_ylim(min(tempInitAire, tempInitBloque) - 5, max(tempInitAire, tempInitBloque) + 5)
        
        line_bloque, = ax.plot([], [], label="Temperatura Bloque", color='red')
        line_aire, = ax.plot([], [], label="Temperatura Aire Salida", color='blue')
        
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Temperatura (°C)")
        ax.legend()

        def actualizar(frame):
            self.transferencia_conveccion_bloque()
            self.historial_tiempo.append(frame)
            self.historial_temp_bloque.append(self.bloque.temperatura)
            self.historial_temp_aire_salida.append(self.aireSalida.temperatura)
            line_bloque.set_data(self.historial_tiempo, self.historial_temp_bloque)
            line_aire.set_data(self.historial_tiempo, self.historial_temp_aire_salida)
            return line_bloque, line_aire

        anim = FuncAnimation(fig, actualizar, frames=range(tiempoSegundos), interval=50, repeat=False)
        plt.show()

def iniciar_simulacion():
    temp_bloque = float(entry_temp_bloque.get())
    temp_aire = float(entry_temp_aire.get())
    velocidad = float(entry_vel_aire.get())
    modelo = TransferenciaCalor()
    modelo.simulacion(300, temp_bloque, temp_aire, velocidad)

# Interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Simulación de Transferencia de Calor")

frame = ttk.Frame(root, padding=20)
frame.grid(row=0, column=0)

# Labels y Entries
ttk.Label(frame, text="Temperatura Inicial del Bloque (°C)").grid(row=0, column=0)
entry_temp_bloque = ttk.Entry(frame)
entry_temp_bloque.grid(row=0, column=1)
entry_temp_bloque.insert(0, "10")

ttk.Label(frame, text="Temperatura Inicial del Aire (°C)").grid(row=1, column=0)
entry_temp_aire = ttk.Entry(frame)
entry_temp_aire.grid(row=1, column=1)
entry_temp_aire.insert(0, "0")

ttk.Label(frame, text="Velocidad del Aire (m/s)").grid(row=2, column=0)
entry_vel_aire = ttk.Entry(frame)
entry_vel_aire.grid(row=2, column=1)
entry_vel_aire.insert(0, "100")

# Botón para iniciar la simulación
btn_simular = ttk.Button(frame, text="Iniciar Simulación", command=iniciar_simulacion)
btn_simular.grid(row=3, column=0, columnspan=2)

root.mainloop()