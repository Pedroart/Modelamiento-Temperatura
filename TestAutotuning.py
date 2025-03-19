import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.signal import lti, lsim

# Definición de clases

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
        self.temperatura = 0
        self.velocidadFlujo = 0
        self.densidad = 1.225  # kg/m³
        self.calorEspecifico = 1.006  # kJ / (°C·kg)
        self.calcularh()

    def calcularh(self):
        self.coeficientePelicula = self.c * np.power(self.velocidadFlujo, 0.5)

class TransferenciaCalor:
    def __init__(self):
        self.bloque = Bloque(1, 1, 1, 900)
        self.aireIngreso = Aire(10, 0.65)
        self.aireSalida = Aire(10, 0.65)

    def transferencia_conveccion_bloque(self):
        h = self.aireIngreso.coeficientePelicula
        Q = h * self.bloque.area * (self.bloque.temperatura - self.aireIngreso.temperatura)

        # Actualización de temperatura del bloque
        self.bloque.temperatura += -Q / (self.bloque.masa * self.bloque.calorEspecifico)

        # Cálculo de temperatura del aire de salida
        dm = self.aireIngreso.densidad * self.aireIngreso.velocidadFlujo * self.bloque.area
        self.aireSalida.temperatura = self.aireIngreso.temperatura + Q / (dm * self.aireIngreso.calorEspecifico)

    def simulacion(self, tempInitBloque, tempInitAire, velAire):

        self.bloque.temperatura = tempInitBloque
        self.aireIngreso.temperatura = tempInitAire
        self.aireIngreso.velocidadFlujo = velAire
        self.aireIngreso.calcularh()

        tiempo = []
        temperaturas_bloque = []
        
        t = 0
        while self.bloque.temperatura > 0.1:
            print(f"Tiempo: {t} s - Temperatura: {self.bloque.temperatura:.2f} °C")
            self.transferencia_conveccion_bloque()
            if t % 10 == 0:  # Guardamos datos cada 10 segundos
                tiempo.append(t)
                temperaturas_bloque.append(self.bloque.temperatura)
            t += 1

        return np.array(tiempo), np.array(temperaturas_bloque)


# Simulación con velocidad de aire de 100 m/s
modelo = TransferenciaCalor()
tiempo, temperatura = modelo.simulacion(10, 0, 100)

# Autotuning del PID con Ziegler-Nichols

def modelo_respuesta(t, K, tau):
    return 10 * np.exp(-t/tau)

def error_pid(params):
    K, tau = params
    temp_modelo = modelo_respuesta(tiempo, K, tau)
    return np.sum((temperatura - temp_modelo) ** 2)

print("Iniciando optimización...")

opt_params = minimize(error_pid, [1, 1], bounds=[(0.1, 10), (0.1, 100)])
K_opt, tau_opt = opt_params.x

# Parámetros del PID (Ziegler-Nichols)
Kp = 1.2 * (tau_opt / K_opt)
Ti = 2 * tau_opt
Td = 0.5 * tau_opt

# Simulación del Control PID
setpoint = 0  # Temperatura deseada en el bloque
tiempo_control = np.arange(0, 300, 1)
temperatura_control = [10]  # Iniciamos en 10°C
error_anterior = 0
integral = 0
velocidad_aire = 50  # Velocidad inicial

print("Iniciando simulación con Control PID...")

for t in tiempo_control[1:]:

    print(f"Tiempo: {t} s - Temperatura: {temperatura_control[-1]:.2f} °C")
    error = setpoint - temperatura_control[-1]
    integral += error
    derivativo = error - error_anterior
    velocidad_aire = Kp * (error + (1/Ti) * integral + Td * derivativo)
    
    # Limitar la velocidad del aire
    velocidad_aire = max(50, min(100, velocidad_aire))
    
    # Simulación con la nueva velocidad de aire
    modelo.aireIngreso.velocidadFlujo = velocidad_aire
    modelo.aireIngreso.calcularh()
    modelo.transferencia_conveccion_bloque()
    
    temperatura_control.append(modelo.bloque.temperatura)
    error_anterior = error

# Graficar resultados
plt.figure(figsize=(8,5))
plt.plot(tiempo, temperatura, label="Enfriamiento sin control", linestyle="dashed")
plt.plot(tiempo_control, temperatura_control, label="Control PID", color="red")
plt.axhline(setpoint, color="black", linestyle="dotted", label="Setpoint")
plt.xlabel("Tiempo (s)")
plt.ylabel("Temperatura (°C)")
plt.legend()
plt.title("Control PID del Bloque")
plt.grid()
plt.show()

print(f"PID Tuned: Kp={Kp:.3f}, Ti={Ti:.3f}, Td={Td:.3f}")
