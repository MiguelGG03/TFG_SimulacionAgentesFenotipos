def simular_juego(jugador1, jugador2, T, S):
    """
    Simula un juego entre jugador1 y jugador2 según la matriz de pagos.
    Cada jugador debe tener ya su estrategia definida ('C' o 'D').
    """
    estrategia1 = jugador1.estrategia
    estrategia2 = jugador2.estrategia

    # Matriz de pagos
    matriz = {
        ('C', 'C'): (1, 1),
        ('C', 'D'): (S, T),
        ('D', 'C'): (T, S),
        ('D', 'D'): (0, 0),
    }

    pago1, pago2 = matriz[(estrategia1, estrategia2)]

    jugador1.pago_acumulado += pago1
    jugador2.pago_acumulado += pago2

    return pago1, pago2  # Por si quieres registrar o visualizar el resultado
