import networkx as nx
import random
import imageio
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Patch 
from collections import Counter
from core.jugador import Jugador

# Colores por fenotipo
colores_fenotipos = {
    'E': 'red',      # Envidioso
    'P': 'blue',     # Pesimista
    'O': 'orange',   # Optimista
    'A': 'green',    # Altruista
    'R': 'purple'    # Aleatorio
}

class ReticulaNX:
    def __init__(self, L, distrib_fenotipos, tau_limites):
        self.L = L
        self.G = nx.grid_2d_graph(L, L, periodic=True)
        self.distrib_fenotipos = distrib_fenotipos
        self.tau_limites = tau_limites
        self._asignar_jugadores()

    def _samplear_fenotipo(self):
        tipos = list(self.distrib_fenotipos.keys())
        pesos = list(self.distrib_fenotipos.values())
        return random.choices(tipos, weights=pesos, k=1)[0]

    def _asignar_jugadores(self):
        for nodo in self.G.nodes:
            id_str = f"{nodo[0]}-{nodo[1]}"
            fenotipo = self._samplear_fenotipo()
            estrategia = None
            tau = random.randint(*self.tau_limites)
            theta = 0
            jugador = Jugador(id_str, fenotipo, estrategia, tau, theta, self.tau_limites)
            self.G.nodes[nodo]['jugador'] = jugador

    def nodos(self):
        return self.G.nodes

    def vecinos(self, nodo):
        return list(self.G.neighbors(nodo))
    
def graficar_y_guardar_fenotipos(reticula, paso, parametros, carpeta="frames"):
    os.makedirs(carpeta, exist_ok=True)

    G = reticula.G
    pos = dict((n, n) for n in G.nodes)

    # Recolectar fenotipos
    fenotipos_actuales = [G.nodes[n]['jugador'].fenotipo for n in G.nodes]
    conteo = Counter(fenotipos_actuales)
    total = sum(conteo.values())

    # Asignar colores por nodo
    colores = []
    for n in G.nodes:
        fenotipo = G.nodes[n]['jugador'].fenotipo
        color = colores_fenotipos.get(fenotipo, 'gray')
        colores.append(color)

    # Crear figura
    #plt.figure(figsize=(10, 9))  # Aumentado ancho para leyenda y texto
    plt.figure(figsize=(12.2, 9.7), dpi=100)
    nx.draw(G, pos=pos, node_color=colores, with_labels=False, node_size=100)

    # Título
    plt.title(f"Fenotipos - PASO {paso + 1}", fontsize=20, pad=20)

    # Leyenda con porcentajes
    leyenda = []
    etiquetas = {
        'E': 'Envidioso',
        'P': 'Pesimista',
        'O': 'Optimista',
        'A': 'Altruista',
        'R': 'Aleatorio'
    }

    for clave in colores_fenotipos:
        porcentaje = (conteo[clave] / total) * 100 if clave in conteo else 0.0
        etiqueta = f"{etiquetas[clave]}: {porcentaje:.1f}%"
        leyenda.append(Patch(color=colores_fenotipos[clave], label=etiqueta))

    plt.legend(handles=leyenda, title="Fenotipos", loc="lower left", bbox_to_anchor=(1.02, 0.3))

        # Texto adicional con parámetros (formato mejorado)
    lineas = []
    for k, v in parametros.items():
        if isinstance(v, list):
            lineas.append(f"{k}:")
            lineas.extend([f"  {item}" for item in v])
        else:
            lineas.append(f"{k} = {v}")
    texto_parametros = "\n".join(lineas)
    plt.gcf().text(1.02, 0.65, texto_parametros, fontsize=9, va='top')

    # Guardar
    filename = os.path.join(carpeta, f"frame_{paso:03d}.png")
    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight')
    plt.close()





def crear_gif(carpeta="img/frames", nombre_salida="simulacion.gif", fps=5):
    imagenes = []
    tamanos = set()

    for archivo in sorted(os.listdir(carpeta)):
        if archivo.lower().endswith('.png'):
            ruta = os.path.join(carpeta, archivo)
            img = imageio.imread(ruta)

            # Convertir RGBA a RGB si es necesario
            if img.shape[2] == 4:
                img = img[:, :, :3]

            tamanos.add(img.shape)
            imagenes.append(img)

    if len(tamanos) > 1:
        raise ValueError(f"❌ Las imágenes no tienen el mismo tamaño: {tamanos}")

    imageio.mimsave(nombre_salida, imagenes, fps=fps)
    print(f"✅ GIF guardado como '{nombre_salida}'")