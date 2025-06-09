import random
from .fenotipos import decidir_estrategia
from math import exp

class Jugador:
    def __init__(self, id, fenotipo, estrategia, tau, theta, tau_limites):
        self.id = id
        self.fenotipo = fenotipo        # 'E', 'O', 'P', 'A', 'R'
        self.fenotipo_anterior = fenotipo
        self.estrategia = estrategia    # 'C' o 'D'
        self.tau = tau                  # Nivel de persistencia actual
        self.theta = theta              # Temporizador
        self.pago_acumulado = 0.0
        self.vecinos = []              # Lista de objetos Jugador
        self.tau_limites = tau_limites # (tauD, tauU)

    def reiniciar_pago(self):
        self.pago_acumulado = 0.0

    def actualizar_theta(self):
        self.theta += 1

    def reiniciar_theta(self):
        self.theta = 0

    def agregar_vecino(self, vecino):
        self.vecinos.append(vecino)

    def decidir_estrategia(self, T, S):
        """Llama a la lógica del fenotipo para decidir si coopera o no."""
        self.estrategia = decidir_estrategia(self.fenotipo, T, S)

    def ajustar_tau(self, phi_local, phi_global, delta_tau, K1):
        """Ajuste de persistencia basado en función tipo Fermi."""
        prob_aumentar = 1 / (1 + exp(-(phi_local - phi_global) / K1))
        if random.random() < prob_aumentar:
            self.tau = min(self.tau + delta_tau, self.tau_limites[1])
        else:
            self.tau = max(self.tau - delta_tau, self.tau_limites[0])

    def considerar_cambio_de_fenotipo(self, K2):
        if self.theta < self.tau:
            self.theta += 1
            return  # No puede cambiar aún

        vecino = random.choice(self.vecinos)
        pi_i = self.pago_acumulado
        pi_j = vecino.pago_acumulado

        prob_imitar = 1 / (1 + exp((pi_i - pi_j) / K2))
        if random.random() < prob_imitar:
            self.fenotipo_anterior = self.fenotipo
            self.fenotipo = vecino.fenotipo

        self.theta = 0  # Reiniciar temporizador tras considerar cambio

