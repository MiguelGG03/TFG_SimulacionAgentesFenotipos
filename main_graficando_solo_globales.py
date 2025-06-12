from config.parametros import *
from core.reticula_nx import ReticulaNX, graficar_fenotipos, guardar_grafico
from core.juego import simular_juego
from utils.matriz_pagos import calcular_pagos_lineales
from utils.visualizacion import graficar_resultados_globales
from utils.crear_estructura import crear_estructura
from utils.logger import inicializar_logger, registrar_estado
from utils.logger_jugadores import registrar_estado_jugadores
from utils.metricas import f_estrategia  # necesario para φ

# EP -
# OA ------

crear_estructura()
inicializar_logger()

# -------------------------------
# PARÁMETROS Y RETÍCULA
# -------------------------------
parametros = {
    "Pasos": pasos,
    "K1": K1,
    "K2": K2,
    "τD": tau_limites[0],
    "τU": tau_limites[1],
    "L": L,
    "Distribucion": [
        f"Envidioso = {int(distrib_fenotipos['E']*100)}%",
        f"Pesimista = {int(distrib_fenotipos['P']*100)}%",
        f"Optimista = {int(distrib_fenotipos['O']*100)}%",
        f"Altruista = {int(distrib_fenotipos['A']*100)}%",
        f"Aleatorio = {int(distrib_fenotipos['R']*100)}%"
    ]
}

reticula = ReticulaNX(L, distrib_fenotipos, tau_limites)

# 💾 Estado inicial (paso 0)
fig_inicial = graficar_fenotipos(reticula, paso=0, parametros=parametros)
guardar_grafico(fig_inicial, "img/estado_inicial.png")

# -------------------------------
# SIMULACIÓN
# -------------------------------
for t in range(pasos):
    for nodo in reticula.nodos():
        reticula.G.nodes[nodo]['jugador'].reiniciar_pago()

    T, S = calcular_pagos_lineales(t, pasos)

    for nodo in reticula.nodos():
        jugador = reticula.G.nodes[nodo]['jugador']
        jugador.decidir_estrategia(T, S)

    # Simular juegos entre pares de vecinos
    for nodo in reticula.nodos():
        jugador1 = reticula.G.nodes[nodo]['jugador']
        for vecino in reticula.vecinos(nodo):
            jugador2 = reticula.G.nodes[vecino]['jugador']
            simular_juego(jugador1, jugador2, T, S)

    # Calcular entorno global φ(t)
    total_coop = sum(f_estrategia(reticula.G.nodes[n]['jugador'].estrategia) for n in reticula.nodos())
    phi_global = total_coop / (L * L)

    # Ajustar τ según entorno local
    for nodo in reticula.nodos():
        jugador = reticula.G.nodes[nodo]['jugador']
        vecinos = [reticula.G.nodes[v]['jugador'] for v in reticula.vecinos(nodo)]
        phi_local = sum(f_estrategia(v.estrategia) for v in vecinos) / len(vecinos)
        jugador.ajustar_tau(phi_local, phi_global, delta_tau, K1)

    # Considerar cambio de fenotipo
    for nodo in reticula.nodos():
        jugador = reticula.G.nodes[nodo]['jugador']
        jugador.vecinos = [reticula.G.nodes[v]['jugador'] for v in reticula.vecinos(nodo)]
        jugador.considerar_cambio_de_fenotipo(K2)

    # Registrar datos
    registrar_estado(reticula, paso=t)
    registrar_estado_jugadores(reticula, paso=t)

# -------------------------------
# RESULTADOS FINALES
# -------------------------------
fig_final = graficar_fenotipos(reticula, paso=pasos, parametros=parametros)
guardar_grafico(fig_final, "img/estado_final.png")
graficar_resultados_globales()
