import random
from core.reticula import Reticula
from core.juego import simular_juego
from utils.metricas import f_estrategia

# -------------------------------
# PARÁMETROS DEL MODELO
# -------------------------------
L = 10  # Tamaño de la retícula (LxL)
pasos = 50  # Número de iteraciones

# Distribución de fenotipos
distrib_fenotipos = {
    'E': 0.30,
    'P': 0.21,
    'O': 0.20,
    'A': 0.17,
    'R': 0.12
}

# Persistencia
tau_limites = (3, 10)
delta_tau = 1
K1 = 0.1  # Sensibilidad al entorno
K2 = 0.1  # Sensibilidad al rendimiento

# -------------------------------
# INICIALIZACIÓN DE LA RETÍCULA
# -------------------------------
reticula = Reticula(L, distrib_fenotipos, tau_limites)

# -------------------------------
# BUCLE PRINCIPAL DE SIMULACIÓN
# -------------------------------
for t in range(pasos):
    print(f"\n--- Paso {t+1} ---")

    # Reiniciar pagos
    for i in range(L):
        for j in range(L):
            reticula.grid[i, j].reiniciar_pago()

    # Generar valores aleatorios para la matriz de pagos
    T = random.uniform(0, 2)
    S = random.uniform(-1, 1)

    # Cada jugador decide su estrategia para esta ronda
    for i in range(L):
        for j in range(L):
            jugador = reticula.grid[i, j]
            jugador.decidir_estrategia(T, S)

    # Simular juegos con cada vecino (una vez por pareja)
    ya_jugado = set()
    for i in range(L):
        for j in range(L):
            jugador = reticula.grid[i, j]
            for vecino in jugador.vecinos:
                pareja = tuple(sorted([jugador.id, vecino.id]))
                if pareja not in ya_jugado:
                    simular_juego(jugador, vecino, T, S)
                    ya_jugado.add(pareja)

    # Calcular entorno global φ(t)
    total_cooperacion = 0
    N = L * L

    for i in range(L):
        for j in range(L):
            jugador = reticula.grid[i, j]
            total_cooperacion += f_estrategia(jugador.estrategia)

    phi_global = total_cooperacion / N

    # Calcular entorno local φi(t) y actualizar τi(t)
    for i in range(L):
        for j in range(L):
            jugador = reticula.grid[i, j]
            suma_local = sum(f_estrategia(vecino.estrategia) for vecino in jugador.vecinos)
            phi_local = suma_local / len(jugador.vecinos)

            jugador.ajustar_tau(phi_local, phi_global, delta_tau, K1)

    print(f"")

# Fin de simulación
