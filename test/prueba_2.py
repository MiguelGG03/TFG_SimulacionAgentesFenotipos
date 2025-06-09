import random
from core.juego import simular_juego
from core.reticula import Reticula



L = 50
distrib = {'E': 0.30, 'P': 0.21, 'O': 0.20, 'A': 0.17, 'R': 0.12}
tau_limites = (3, 10)

reticula = Reticula(L, distrib, tau_limites)

jugador1 = reticula.obtener_jugador(0, 0)
jugador2 = reticula.obtener_jugador(49, 0)

print(f"Fenotipo : {jugador1.fenotipo}")
print(f"Coordenadas vecinos {[v.id for v in jugador1.vecinos]}")

print(f"Fenotipo : {jugador2.fenotipo}")
print(f"Coordenadas vecinos {[v.id for v in jugador2.vecinos]}")

# Valores aleatorios de S y T
S = random.uniform(-1, 1)
T = random.uniform(0, 2)

print(f"T : {T}")
print(f"S : {S}")

jugador1.decidir_estrategia(T, S)
jugador2.decidir_estrategia(T, S)

pago1,pago2 = simular_juego(jugador1, jugador2, T, S)

print(f"Pago Jugador 1: {pago1}")
print(f"Pago Jugador 2: {pago2}")
