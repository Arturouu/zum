# Camino más corto entre intersecciones - Técnica: Algoritmo de Dijkstra
#
# Sustento:
#  - Las intersecciones son nodos y los tramos de calle son aristas dirigidas con un
#    costo (su longitud en metros): grafo dirigido y ponderado.
#  - Se busca el camino de menor distancia total (no el de menos tramos) y todas las
#    longitudes son positivas, que es la condición de Dijkstra.
#  - Dijkstra con cola de prioridad (heapq) expande siempre el nodo de menor costo
#    acumulado, así la primera vez que se saca un nodo su costo ya es el mínimo.
#  - Complejidad: O((V + E) log V) por ejecución.
#
# Para la ruta de Zum se ejecuta una vez desde el origen y una vez desde cada entrega
# (n + 1 ejecuciones) y con eso se arma la matriz de distancias entre todos los puntos.
# Como el grafo es dirigido, la matriz no es simétrica: D[i][j] puede ser != D[j][i].

import heapq as hq
import math


# 1. Algoritmo de Dijkstra
def dijkstra(G: list[list[tuple[int, float]]], s: int) -> tuple[list[int | None], list[float]]:
    """
    Distancia mínima desde s hacia todos los nodos de G.
    Devuelve (path, cost): path[v] es el nodo anterior a v en el camino más corto y
    cost[v] la distancia mínima de s a v (math.inf si no se puede llegar).
    """
    n = len(G)
    visited = [False] * n
    path = [None] * n
    cost = [math.inf] * n
    cost[s] = 0
    queue = [(0, s)]
    while queue:
        g_u, u = hq.heappop(queue)
        if not visited[u]:
            visited[u] = True
            for v, w in G[u]:
                f = g_u + w
                if f < cost[v]:
                    cost[v] = f
                    path[v] = u
                    hq.heappush(queue, (f, v))
    return path, cost


# 2. Reconstruir la ruta desde el destino usando path
def get_route(path: list[int | None], t: int) -> list[int]:
    """Lista de nodos desde el origen de Dijkstra hasta t, en orden."""
    route = []
    while t is not None:
        route.append(t)
        t = path[t]
    return route[::-1]


# 3. Matriz de distancias entre los puntos de la ruta
def matriz_distancias(
    G: list[list[tuple[int, float]]], puntos: list[int]
) -> tuple[list[list[float]], list[list[int | None]]]:
    """
    puntos[0] es el origen y puntos[1:] las entregas (índices de nodos del grafo).
    Ejecuta Dijkstra desde cada punto y devuelve:
      D[i][j]  distancia mínima del punto i al punto j (en metros)
      paths[i] el arreglo path de Dijkstra desde el punto i, para reconstruir luego
               el camino calle por calle con get_route(paths[i], puntos[j])
    """
    D = []
    paths = []
    for s in puntos:
        path, cost = dijkstra(G, s)
        D.append([cost[t] for t in puntos])
        paths.append(path)
    return D, paths
