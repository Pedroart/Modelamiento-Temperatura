import numpy as np
import matplotlib.pyplot as plt

class BateriaRefrigeracion:
    def __init__(self, area, coef_transferencia, masa_aire, masa_ref, cp_aire, cp_ref):
        self.area = area  # Área de intercambio térmico (m²)
        self.U = coef_transferencia  # Coeficiente de transferencia de calor (W/m²K)
        self.masa_aire = masa_aire  # Flujo de masa del aire (kg/s)
        self.masa_ref = masa_ref  # Flujo de masa del refrigerante (kg/s)
        self.cp_aire = cp_aire  # Capacidad calorífica del aire (J/kgK)
        self.cp_ref = cp_ref  # Capacidad calorífica del refrigerante (J/kgK)
        self.temp_aire = None
        self.temp_ref = None

    def transferencia_calor(self):
        # Cálculo de la potencia de intercambio térmico
        Q = self.U * self.area * (self.temp_aire - self.temp_ref)

        # Cambio de temperatura en el aire
        dT_aire = -Q / (self.masa_aire * self.cp_aire)
        self.temp_aire += dT_aire

        # Cambio de temperatura en el refrigerante
        dT_ref = Q / (self.masa_ref * self.cp_ref)
        #self.temp_ref += dT_ref

    def simulacion(self, tiempo_simulacion, temp_init_aire, temp_init_ref):
        self.temp_aire = temp_init_aire
        self.temp_ref = temp_init_ref

        tiempo = np.arange(0, tiempo_simulacion + 1, 1)
        temperaturas_aire = [self.temp_aire]
        temperaturas_ref = [self.temp_ref]

        for _ in tiempo[1:]:
            self.transferencia_calor()
            temperaturas_aire.append(self.temp_aire)
            temperaturas_ref.append(self.temp_ref)

        return tiempo, temperaturas_aire, temperaturas_ref


# Parámetros del sistema
area = 2.0  # m²
U = 20  # W/(m²·K)
masa_aire = 0.5  # kg/s
masa_ref = 0.2  # kg/s
cp_aire = 1005  # J/(kg·K)
cp_ref = 4180  # J/(kg·K)

# Condiciones iniciales
temp_init_aire = 30.0  # °C
temp_init_ref = 10.0  # °C
tiempo_simulacion = 300  # s

# Crear objeto y ejecutar simulación
bateria = BateriaRefrigeracion(area, U, masa_aire, masa_ref, cp_aire, cp_ref)
tiempo, temperaturas_aire, temperaturas_ref = bateria.simulacion(tiempo_simulacion, temp_init_aire, temp_init_ref)

# Graficar resultados
plt.figure(figsize=(10, 5))
plt.plot(tiempo, temperaturas_aire, label="Temperatura del aire (°C)", color="red")
plt.plot(tiempo, temperaturas_ref, label="Temperatura del refrigerante (°C)", color="blue", linestyle="dashed")
plt.xlabel("Tiempo (s)")
plt.ylabel("Temperatura (°C)")
plt.title("Evolución de las temperaturas en la batería de refrigeración")
plt.legend()
plt.grid()
plt.show()
