import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import control as ctrl
from scipy.integrate import solve_ivp
import tkinter as tk
from tkinter import ttk

class EnfriadorGlicol:
    def __init__(self):
        # Propiedades del glicol
        self.Cp_glicol = 2.43 * 1000  # J/kgK
        self.rho_glicol = 1110  # kg/m³
        self.k_glicol = 0.25  # W/mK
        self.mu_glicol = 0.005  # Pa.s
        
        # Propiedades del aire
        self.Cp_aire = 1005  # J/kgK
        self.rho_aire = 1.225  # kg/m³
        self.k_aire = 0.026  # W/mK
        self.mu_aire = 1.85e-5  # Pa.s

        # Parámetros de geometría
        self.L = 1.0  # Longitud característica (m)
        self.A = 1.0  # Área de intercambio térmico (m²)
        
        # Variables dinámicas
        self.T_glicol_entrada = 80  # °C
        self.T_glicol_salida = 60  # °C
        self.T_aire_entrada = 20  # °C
        self.T_aire_salida = 0  # °C (se calculará)
        self.vel_aire = 5  # m/s
        self.vel_glicol = 1  # m/s
        self.Q = 0  # Energía transferida
    
    def calcular_intercambio(self):
        # Flujo másico
        m_dot_glicol = self.rho_glicol * self.vel_glicol * self.A
        m_dot_aire = self.rho_aire * self.vel_aire * self.A
        
        # Números adimensionales
        Re_glicol = (self.rho_glicol * self.vel_glicol * self.L) / self.mu_glicol
        Re_aire = (self.rho_aire * self.vel_aire * self.L) / self.mu_aire
        Pr_glicol = (self.Cp_glicol * self.mu_glicol) / self.k_glicol
        Pr_aire = (self.Cp_aire * self.mu_aire) / self.k_aire

        # Nusselt (flujo turbulento en tuberías)
        Nu_glicol = 0.023 * Re_glicol**0.8 * Pr_glicol**0.4
        Nu_aire = 0.023 * Re_aire**0.8 * Pr_aire**0.4

        # Coeficientes de convección
        h_glicol = (Nu_glicol * self.k_glicol) / self.L
        h_aire = (Nu_aire * self.k_aire) / self.L

        # Coeficiente global de transferencia de calor
        U = 1 / (1/h_glicol + 1/h_aire)

        # Diferencia de temperatura logarítmica
        delta_T1 = self.T_glicol_entrada - self.T_aire_entrada
        delta_T2 = self.T_glicol_salida - self.T_aire_salida
        delta_T_log = (delta_T1 - delta_T2) / np.log(delta_T1 / delta_T2)

        # Cálculo de Q (energía transferida)
        self.Q = U * self.A * delta_T_log

        # Calcular temperatura de salida del aire
        self.T_aire_salida = self.T_aire_entrada + self.Q / (m_dot_aire * self.Cp_aire)
        return self.Q, self.T_aire_salida

# Simulación con Control PID
def pid_control(Kp, Ki, Kd, T_setpoint, tiempo):
    modelo = EnfriadorGlicol()
    modelo.T_glicol_entrada = T_setpoint
    dt = 1
    T_actual = modelo.T_glicol_salida
    historial = []
    error_acumulado = 0
    error_anterior = 0
    
    for t in range(tiempo):
        error = T_setpoint - T_actual
        error_acumulado += error * dt
        error_derivado = (error - error_anterior) / dt
        control = Kp * error + Ki * error_acumulado + Kd * error_derivado
        
        modelo.vel_aire = max(1, min(10, modelo.vel_aire + control))
        modelo.calcular_intercambio()
        T_actual = modelo.T_aire_salida
        historial.append(T_actual)
        error_anterior = error
    
    return historial

# Ejecutar simulación y graficar
historial = pid_control(Kp=0.5, Ki=0.1, Kd=0.05, T_setpoint=40, tiempo=100)
plt.plot(historial, label="Temperatura Aire Salida")
plt.xlabel("Tiempo (s)")
plt.ylabel("Temperatura (°C)")
plt.legend()
plt.show()
