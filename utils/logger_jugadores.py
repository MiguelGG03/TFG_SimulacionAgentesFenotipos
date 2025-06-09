import csv
import os

def inicializar_logger_jugadores(path="resultados/logs/log_jugadores.csv"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, mode='w', newline='') as archivo:
        writer = csv.writer(archivo)
        writer.writerow([
            'paso', 'id', 'fenotipo', 'cambio_fenotipo',
            'estrategia', 'pago', 'tau', 'theta'
        ])

def registrar_estado_jugadores(reticula, paso, path="resultados/logs/log_jugadores.csv"):
    with open(path, mode='a', newline='') as archivo:
        writer = csv.writer(archivo)
        for nodo in reticula.nodos():
            jugador = reticula.G.nodes[nodo]['jugador']
            cambio = jugador.fenotipo != getattr(jugador, 'fenotipo_anterior', jugador.fenotipo)
            writer.writerow([
                paso,
                jugador.id,
                jugador.fenotipo,
                int(cambio),
                jugador.estrategia,
                round(jugador.pago_acumulado, 3),
                jugador.tau,
                jugador.theta
            ])
            jugador.fenotipo_anterior = jugador.fenotipo  # actualizar para el siguiente paso
