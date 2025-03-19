import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
class Fluido:
    def __init__(self, nombre, temperatura, densidad, calor_especifico, velocidad_flujo=None):
        self.nombre = nombre
        self.temperatura = temperatura  # °C
        self.densidad = densidad  # kg/m³
        self.calor_especifico = calor_especifico  # J/kg·K
        self.velocidad_flujo = velocidad_flujo  # m/s si aplica

class Intercambiador:
    def __init__(self, area, eficiencia, flujo_glicol, flujo_aire):
        self.area = area  # m²
        self.eficiencia = eficiencia  # Factor de eficiencia del intercambiador
        self.flujo_glicol = flujo_glicol  # kg/s
        self.flujo_aire = flujo_aire  # kg/s

    def transferencia_calor(self, glicol, aire):
        # Cálculo del calor transferido
        Q = self.eficiencia * self.area * (glicol.temperatura - aire.temperatura) * 500  # Ajuste de coeficiente
        
        # Actualizar temperaturas usando balance de energía
        glicol.temperatura -= Q / (self.flujo_glicol * glicol.calor_especifico)
        aire.temperatura += Q / (self.flujo_aire * aire.calor_especifico)

class Simulador:
    def __init__(self, glicol, aire, intercambiador):
        self.glicol = glicol
        self.aire = aire
        self.intercambiador = intercambiador

    def ejecutar(self, tiempo_segundos):
        historial = []
        for t in range(tiempo_segundos):
            self.intercambiador.transferencia_calor(self.glicol, self.aire)
            historial.append((t, self.glicol.temperatura, self.aire.temperatura))

        return historial

# Definir propiedades de los fluidos
glicol = Fluido(nombre="Glicol", temperatura=-6, densidad=1050, calor_especifico=3850)  # kg/m³, J/kg·K
aire = Fluido(nombre="Aire", temperatura=30, densidad=1.2, calor_especifico=1005, velocidad_flujo=2.0)  # kg/m³, J/kg·K

# Crear intercambiador de calor
intercambiador = Intercambiador(area=5, eficiencia=0.85, flujo_glicol=0.5, flujo_aire=2.5)

# Crear simulador y ejecutar
simulador = Simulador(glicol, aire, intercambiador)
historial = simulador.ejecutar(tiempo_segundos=100)

# Convertir resultados en DataFrame y mostrar
df_resultados = pd.DataFrame(historial, columns=["Tiempo (s)", "Temp Glicol (°C)", "Temp Aire (°C)"])

# Graficar resultados
plt.figure(figsize=(10, 5))
plt.plot(df_resultados["Tiempo (s)"], df_resultados["Temp Glicol (°C)"], label="T Glicol")
plt.plot(df_resultados["Tiempo (s)"], df_resultados["Temp Aire (°C)"], label="T Aire", linestyle="dashed")

plt.xlabel("Tiempo (s)")
plt.ylabel("Temperatura (°C)")
plt.title("Evolución de la Temperatura en el Tiempo")
plt.legend()
plt.grid()
plt.show()
