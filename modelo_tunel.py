import numpy as np
import matplotlib.pyplot as plt

class Fluido:
    def __init__(self, densidad, cp, temperatura):
        self.densidad = densidad
        self.cp = cp
        self.temperatura = temperatura

class Refrigerante(Fluido):
    def __init__(self, densidad=997, cp=4180, temperatura=10.0):
        super().__init__(densidad, cp, temperatura)

class Aire(Fluido):
    def __init__(self, c, velocidad_flujo=100, temperatura=16.0):
        super().__init__(densidad=1.225, cp=1006, temperatura=temperatura)
        self.c = c
        self.velocidad_flujo = velocidad_flujo
        self.h = self.calcular_coeficiente()
    
    def calcular_coeficiente(self):
        return self.c * np.power(self.velocidad_flujo, 0.5)

class Bloque:
    def __init__(self, ancho, alto, masa, calor_especifico, temperatura=20):
        self.ancho = ancho
        self.alto = alto
        self.masa = masa
        self.calor_especifico = calor_especifico
        self.area = ancho * alto
        self.temperatura = temperatura

class ProcesoIntercambioCalor:
    def __init__(self, aire, refrigerante, area, coef_transferencia):
        self.aire = aire
        self.refrigerante = refrigerante
        self.area = area
        self.U = coef_transferencia
    
    def transferencia_calor(self):
        Q = self.U * self.area * (self.aire.temperatura - self.refrigerante.temperatura)
        
        dm = self.aire.densidad * self.aire.velocidad_flujo * self.area
        dT_aire = -Q / (dm * self.aire.cp)
        self.aire.temperatura += dT_aire
        
        
        dT_ref = Q / (self.refrigerante.densidad * self.refrigerante.cp)
        self.refrigerante.temperatura += dT_ref

class ProcesoConveccion:
    def __init__(self, bloque, aire):
        self.bloque = bloque
        self.aire = aire
    
    def transferencia_conveccion(self):
        h = self.aire.h
        Q = h * self.bloque.area * (self.bloque.temperatura - self.aire.temperatura)
        self.bloque.temperatura += -Q / (self.bloque.masa * self.bloque.calor_especifico)
        dm = self.aire.densidad * self.aire.velocidad_flujo * self.bloque.area
        self.aire.temperatura += Q / (dm * self.aire.cp)

# Parámetros
area = 2.0
U = 20
temp_init_aire = 16
temp_init_ref = 10.0
tiempo_simulacion = 300

# Instancias
refrigerante = Refrigerante(temperatura=temp_init_ref)
aire = Aire(10, temperatura=temp_init_aire)
bateria = ProcesoIntercambioCalor(aire, refrigerante, area, U)
masa_termica = ProcesoConveccion(Bloque(1, 1, 1, 900,17), aire)

# Simulación
temps_aire = []
temps_bloque = []

def simular():
    for _ in range(tiempo_simulacion):
        bateria.transferencia_calor()
        masa_termica.transferencia_conveccion()
        
        temps_aire.append(bateria.aire.temperatura)
        temps_bloque.append(masa_termica.bloque.temperatura)

simular()

# Gráficos
plt.figure(figsize=(10, 5))
plt.plot(range(tiempo_simulacion), temps_aire, label='Temperatura del Aire (°C)')
plt.plot(range(tiempo_simulacion), temps_bloque, label='Temperatura del Bloque (°C)')
plt.xlabel('Tiempo (s)')
plt.ylabel('Temperatura (°C)')
plt.title('Evolución de la Temperatura')
plt.legend()
plt.grid()
plt.show()