import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize, curve_fit

# Definición de clases

class Bloque:
    def __init__(self, ancho, alto, masa, calorEspecifico):
        self.ancho = ancho
        self.alto = alto
        self.masa = max(masa, 0.1)  # Evitar masa cero
        self.calorEspecifico = calorEspecifico
        self.area = ancho * alto
        self.temperatura = 0

class Aire:
    def __init__(self, c):
        self.c = c
        self.velocidadFlujo = 0.1  # Evitar velocidad cero
        self.densidad = 1.225  # kg/m³
        self.calorEspecifico = 1.006  # kJ/(°C·kg)
        self.temperatura = 0
        self.coeficientePelicula = 0

    def calcularh(self):
        self.coeficientePelicula = max(self.c * np.sqrt(self.velocidadFlujo), 0.1)  # Evitar h=0

class TransferenciaCalor:
    def __init__(self):
        self.bloque = Bloque(1, 1, 1, 900)
        self.aireIngreso = Aire(10)
        self.aireSalida = Aire(10)

    def transferencia_conveccion_bloque(self):
        h = self.aireIngreso.coeficientePelicula
        if np.isnan(h) or h <= 0:
            return

        Q = h * self.bloque.area * (self.bloque.temperatura - self.aireIngreso.temperatura)
        self.bloque.temperatura -= Q / (self.bloque.masa * self.bloque.calorEspecifico)
        
        dm = self.aireIngreso.densidad * self.aireIngreso.velocidadFlujo * self.bloque.area
        if dm > 0:
            self.aireSalida.temperatura = self.aireIngreso.temperatura + Q / (dm * self.aireIngreso.calorEspecifico)

    def simulacion(self, tempInitBloque, tempInitAire, velAire):
        self.bloque.temperatura = tempInitBloque
        self.aireIngreso.temperatura = tempInitAire
        self.aireIngreso.velocidadFlujo = max(velAire, 0.1)  # Evitar velocidad cero
        self.aireIngreso.calcularh()

        tiempo = []
        temperaturas_bloque = []
        t = 0

        while self.bloque.temperatura > 0.1 and t < 1000:
            self.transferencia_conveccion_bloque()
            if t % 10 == 0:
                tiempo.append(t)
                temperaturas_bloque.append(self.bloque.temperatura)
            t += 1

        return np.array(tiempo), np.array(temperaturas_bloque)

modelo = TransferenciaCalor()
tiempo, temperatura = modelo.simulacion(10, 0, 100)

# Estimación del modelo de primer orden
def modelo_fopdt(t, K, tau):
    return K * (1 - np.exp(-t / tau))

params_opt, _ = curve_fit(modelo_fopdt, tiempo, temperatura, bounds=([0.1, 0.1], [10, 100]))
K_opt, tau_opt = params_opt

# Simulación del Control PID con parámetros optimizados
modelo = TransferenciaCalor()
modelo.bloque.temperatura = 10

temperatura_control = [modelo.bloque.temperatura]
error_anterior = 0
integral = 0
velocidad_aire = 50
setpoint = 5

tiempo_control = np.arange(0, 100, 1)

for t in tiempo_control[1:]:
    error = setpoint - modelo.bloque.temperatura
    integral += error
    derivativo = error - error_anterior
    velocidad_aire = max(10, min(200, Kp_opt * (error + (1 / Ti_opt) * integral + Td_opt * derivativo)))
    
    modelo.aireIngreso.velocidadFlujo = velocidad_aire
    modelo.aireIngreso.calcularh()
    modelo.transferencia_conveccion_bloque()
    
    temperatura_control.append(modelo.bloque.temperatura)
    error_anterior = error

# Graficar resultados
plt.figure(figsize=(10, 6))
plt.plot(tiempo, temperatura, label="Enfriamiento sin control", linestyle="dashed", color="blue")
plt.plot(tiempo_control, temperatura_control, label="Con PID Optimizado", color="red")
plt.axhline(setpoint, color="black", linestyle="dotted", label="Setpoint (5°C)")
plt.xlabel("Tiempo (s)")
plt.ylabel("Temperatura (°C)")
plt.title("Comparación de Respuesta del Sistema con y sin PID")
plt.legend()
plt.grid()
plt.show()

print(f"Modelo Estimado: K={K_opt:.3f}, Tau={tau_opt:.3f}")
print(f"PID Optimizado (ITAE): Kp={Kp_opt:.3f}, Ti={Ti_opt:.3f}, Td={Td_opt:.3f}")
