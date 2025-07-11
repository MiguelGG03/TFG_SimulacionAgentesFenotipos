import pandas as pd
from config.parametros import *
from core.reticula_nx import *
from core.juego import simular_juego
from utils.crear_estructura import crear_estructura
from utils.metricas import f_estrategia
from utils.logger import inicializar_logger, registrar_estado
from utils.logger_jugadores import inicializar_logger_jugadores, registrar_estado_jugadores
from utils.visualizacion import graficar_resultados_globales, graficar_rendimiento_jugador
from utils.resize_imagenes import pad_imagenes_en_carpeta
from utils.matriz_pagos import calcular_pagos_lineales

crear_estructura()
inicializar_logger()
inicializar_logger_jugadores()

# -------------------------------
# PARÁMETROS DEL MODELO
# -------------------------------

"""
Los parametros son inicializados desde el archivo 'config/parametros.py'.
"""

parametros = {
    "Pasos": pasos,
    "K1": K1,  # Factor de ajuste de τ según φ
    "K2": K2,  # Factor de cambio de fenotipo
    "τD": tau_limites[0],  # Valor mínimo de τ
    "τU": tau_limites[1],  # Valor máximo de τ
    "L": L,
    "Distribucion": [
        f"Envidioso = {int(round(distrib_fenotipos['E']*100,0))}%",
        f"Pesimista = {int(round(distrib_fenotipos['P']*100,0))}%",
        f"Optimista = {int(round(distrib_fenotipos['O']*100,0))}%",
        f"Altruista = {int(round(distrib_fenotipos['A']*100,0))}%",
        f"Aleatorio = {int(round(distrib_fenotipos['R']*100,0))}%"
    ]
}


# -------------------------------
# INICIALIZACIÓN DE LA RETÍCULA
# -------------------------------
reticula = ReticulaNX(L, distrib_fenotipos, tau_limites)

# -------------------------------
# SIMULACIÓN
# -------------------------------

graficar_y_guardar_fenotipos(reticula, paso=0, parametros=parametros, carpeta='img/frames')

for t in range(pasos):
    print(f"--- Paso {t+1} ---")

    # Reiniciar pagos
    for nodo in reticula.nodos():
        reticula.G.nodes[nodo]['jugador'].reiniciar_pago()

    T, S = calcular_pagos_lineales(t, pasos)

    # Decidir estrategias
    for nodo in reticula.nodos():
        jugador = reticula.G.nodes[nodo]['jugador']
        jugador.decidir_estrategia(T, S)

    # Simular juegos entre pares (evitando repeticiones)
    jugadas = set()
    for nodo in reticula.nodos():
        jugador = reticula.G.nodes[nodo]['jugador']
        for vecino_nodo in reticula.vecinos(nodo):
            par = tuple(sorted([nodo, vecino_nodo]))
            if par not in jugadas:
                vecino = reticula.G.nodes[vecino_nodo]['jugador']
                simular_juego(jugador, vecino, T, S)
                jugadas.add(par)

    # Calcular entorno global φ(t)
    total_coop = sum(f_estrategia(reticula.G.nodes[n]['jugador'].estrategia) for n in reticula.nodos())
    phi_global = total_coop / (L * L)

    # Actualizar τ según entorno local
    for nodo in reticula.nodos():
        jugador = reticula.G.nodes[nodo]['jugador']
        vecinos = [reticula.G.nodes[v]['jugador'] for v in reticula.vecinos(nodo)]
        suma_local = sum(f_estrategia(v.estrategia) for v in vecinos)
        phi_local = suma_local / len(vecinos)
        jugador.ajustar_tau(phi_local, phi_global, delta_tau, K1)

    # Considerar cambio de fenotipo si θ ≥ τ
    for nodo in reticula.nodos():
        jugador = reticula.G.nodes[nodo]['jugador']
        jugador.vecinos = [reticula.G.nodes[v]['jugador'] for v in reticula.vecinos(nodo)]
        jugador.considerar_cambio_de_fenotipo(K2)

    # Guardar frame visual por fenotipo
    if t == 0:
        pass
    else:
        graficar_y_guardar_fenotipos(reticula, paso=t, parametros=parametros, carpeta='img/frames')
    registrar_estado(reticula, paso=t)
    registrar_estado_jugadores(reticula, paso=t)


# -------------------------------
# CREAR GIF FINAL
# -------------------------------

pad_imagenes_en_carpeta(carpeta='img/frames')

crear_gif(carpeta='img/frames', nombre_salida='simulacion.gif', fps=5)


# -------------------------------
# GRAFICAR LOS RESULTADOS
# -------------------------------

graficar_resultados_globales()
jugadores = pd.read_csv('resultados/logs/log_jugadores.csv')
jugadores = jugadores['id'].unique()

for jugador_id in jugadores:
    graficar_rendimiento_jugador(jugador_id=jugador_id)