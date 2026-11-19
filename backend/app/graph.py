# Grafo vial de Santiago de Surco
#
# Modelo:
#  - Nodos: intersecciones (3854). Aristas: tramos de calle dirigidos (9008).
#  - Peso de cada arista: su longitud en metros (columna "length"). Solo distancia,
#    sin tiempo ni tráfico.
#  - Es dirigido porque hay calles de un solo sentido (una calle de doble sentido
#    aparece como dos aristas, u -> v y v -> u).
#  - Representación: lista de adyacencia ponderada, como en los ejercicios del curso:
#      labels[i] = osmid del nodo i      w2i[osmid] = i      G[u] = [(v, w), ...]
#    Para 3854 nodos y 9008 aristas es mucho más liviana que una matriz de 3854 x 3854.

import csv
import math
from dataclasses import dataclass
from pathlib import Path

CARPETA_DATASET = Path(__file__).resolve().parents[2] / "dataset"


@dataclass
class Grafo:
    labels: list[int]                         # índice -> osmid
    w2i: dict[int, int]                       # osmid -> índice
    coords: list[tuple[float, float]]         # índice -> (lon, lat)
    G: list[list[tuple[int, float]]]          # lista de adyacencia: G[u] = [(v, metros), ...]

    @property
    def num_nodos(self) -> int:
        return len(self.G)

    @property
    def num_aristas(self) -> int:
        return sum(len(adyacentes) for adyacentes in self.G)


# 1. Leer los CSV y construir la lista de adyacencia ponderada
def cargar_grafo(carpeta: Path = CARPETA_DATASET) -> Grafo:
    """Lee nodos.csv y aristas.csv (generados con OSMnx) y arma el grafo."""
    labels = []
    w2i = dict()
    coords = []
    with open(carpeta / "nodos.csv", encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            osmid = int(fila["osmid"])
            w2i[osmid] = len(labels)
            labels.append(osmid)
            coords.append((float(fila["x"]), float(fila["y"])))

    G = [[] for _ in labels]
    with open(carpeta / "aristas.csv", encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            u = w2i[int(fila["u"])]
            v = w2i[int(fila["v"])]
            G[u].append((v, float(fila["length"])))

    return Grafo(labels, w2i, coords, G)


# 2. Distancia en línea recta entre dos puntos [lon, lat] (fórmula de haversine), en metros
def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    R = 6371000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


# 3. Nodo del grafo más cercano a un punto marcado en el mapa
def nodo_mas_cercano(grafo: Grafo, lon: float, lat: float) -> tuple[int, float]:
    """
    Devuelve (índice del nodo, distancia en metros) del nodo más cercano a (lon, lat).
    Búsqueda lineal: compara contra los 3854 nodos, O(V). Con tan pocos nodos tarda ~ms.
    """
    mejor, mejor_d = -1, math.inf
    for i, (x, y) in enumerate(grafo.coords):
        d = haversine(lon, lat, x, y)
        if d < mejor_d:
            mejor, mejor_d = i, d
    return mejor, mejor_d
