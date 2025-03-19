import numpy as np
import matplotlib.pyplot as plt

# Parámetros del modelo
dx = 0.01  # Tamaño del paso espacial (m)
dt = 1     # Paso de tiempo (s)
L = 0.1    # Tamaño del producto (m)
T_air = -40 # Temperatura del aire (°C)
T_init = 5  # Temperatura inicial del producto (°C)
T_freeze = -5  # Temperatura de congelación del producto (°C)
k = 0.5   # Conductividad térmica (W/m·K)
rho = 900  # Densidad del producto (kg/m³)
c_p = 2.5  # Capacidad calorífica específica (J/g·K)
L_f = 330  # Calor latente de fusión (J/g)
h = 50     # Coeficiente de convección (W/m²·K)

# Discretización
Nx = int(L/dx)  # Número de puntos espaciales
T = np.ones(Nx) * T_init  # Temperatura inicial del producto
alpha = k / (rho * c_p)  # Difusividad térmica
r = alpha * dt / dx**2  # Número de Fourier

# Simulación
time_steps = 3600  # 1 hora de simulación
time = np.arange(0, time_steps, dt)

for t in time:
    T_new = T.copy()
    
    for i in range(1, Nx-1):
        T_new[i] = T[i] + r * (T[i+1] - 2*T[i] + T[i-1])
    
    # Condición de frontera (superficie expuesta al aire)
    T_new[0] = T[0] + (h * dt / (rho * c_p * dx)) * (T_air - T[0])
    
    # Cambio de fase (modelo simplificado)
    freezing_indices = np.where((T >= T_freeze) & (T_new < T_freeze))
    T_new[freezing_indices] = T_freeze
    
    T = T_new.copy()

# Visualización de resultados
plt.plot(np.linspace(0, L, Nx), T, label='Temperatura final')
plt.axhline(y=T_freeze, color='r', linestyle='--', label='Punto de congelación')
plt.xlabel('Posición en el producto (m)')
plt.ylabel('Temperatura (°C)')
plt.title('Distribución de temperatura en el producto después de 1 hora')
plt.legend()
plt.grid()
plt.show()
