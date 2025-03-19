import numpy as np

class Bloque:

    # parametros del bloque (representacion 2D)
    masa =0
    ancho = 0
    alto = 0
    area = 0
    longitudCaracteristica = 0
    
    calorEspecifico = 0
    temperatura = 0

    def __init__(self, ancho,alto,masa,calorEspecifico):
        self.ancho = ancho
        self.alto = alto
        self.masa = masa
        self.calorEspecifico = calorEspecifico

        self.area = ancho * alto
        

class Aire:
    
    temperatura = 0
    coeficientePelicula = 0 # h

    c = 5 # puede ir de 5 a 25
    n = 0.5 # puede ir de 0.5 a 0.8 (laminar a turbular)

    velocidadFlujo = 0

    densidad = 1.225 # kg/m3
    calorEspecifico = 1.006 # KJ / C*Kg

    def __init__(self,c,h):
        self.c = c
        self.h = h
        self.calcularh()

    def calcularh(self): 
        self.coeficientePelicula = self.c * np.power(self.velocidadFlujo,self.n)



class TransferenciaCalor:

    def __init__(self):
        self.bloque = Bloque(1,1,1,900)
        self.aireIngreso = Aire(10,0.65)
        self.aireSalida  = Aire(10,0.65)

    def transferencia_conveccion_bloque(self):
        v = self.aireIngreso.velocidadFlujo
        h = self.aireIngreso.coeficientePelicula

        # Haciendo un Balance de energia, la energia de lleva el aire es la energia que le quita el bloque
        # dE = Qaire - Qbloque = 0
        # Qaire = Qbloque
    
        Q = h * self.bloque.area * (self.bloque.temperatura - self.aireIngreso.temperatura) 

        # Energia Bloque
        # m*ce*dT =  Qsalida
        self.bloque.temperatura +=  - Q / (self.bloque.masa * self.bloque.calorEspecifico)

        # Energia Aire Salida
        # dm * ce * dt = Qsalida
        dm = self.aireIngreso.densidad *self.aireIngreso.velocidadFlujo*self.bloque.area
        self.aireSalida.temperatura = self.aireIngreso.temperatura + Q / (dm* self.aireIngreso.calorEspecifico)

        
    def simulacion(self, tiempoSegundos, tempInitBloque, tempInitAire, velAire = 100):

        self.bloque.temperatura = tempInitBloque
        self.aireIngreso.temperatura = tempInitAire
        self.aireIngreso.velocidadFlujo = velAire
        self.aireIngreso.calcularh()

        for t in range(0,tiempoSegundos):
            self.transferencia_conveccion_bloque()

            print(f"Temp bloque: {self.bloque.temperatura}")
            print(f"Temp Aire Salida: {self.aireSalida.temperatura}")
        

if __name__ == "__main__":
    modelo = TransferenciaCalor()
    modelo.simulacion(300,10,0)