from core.reticula import Reticula

L = 50
distrib = {'E': 0.30, 'P': 0.21, 'O': 0.20, 'A': 0.17, 'R': 0.12}
tau_limites = (3, 10)

reticula = Reticula(L, distrib, tau_limites)

jugador = reticula.obtener_jugador(0, 0)
print(f"Fenotipo : {jugador.fenotipo}")
print(f"Coordenadas vecinos {[v.id for v in jugador.vecinos]}")
