import math

from app.dijkstra import dijkstra, get_route, matriz_distancias

# Grafo dirigido pequeño:
#   0 -> 1 (4)   0 -> 2 (1)   2 -> 1 (2)   1 -> 3 (1)   2 -> 3 (5)   3 -> 0 (7)
G = [
    [(1, 4), (2, 1)],
    [(3, 1)],
    [(1, 2), (3, 5)],
    [(0, 7)],
]


def test_dijkstra_encuentra_las_distancias_minimas():
    _, cost = dijkstra(G, 0)
    assert cost == [0, 3, 1, 4]


def test_get_route_reconstruye_el_camino():
    path, _ = dijkstra(G, 0)
    assert get_route(path, 3) == [0, 2, 1, 3]
    assert get_route(path, 0) == [0]


def test_nodo_inalcanzable_queda_en_infinito():
    path, cost = dijkstra([[(1, 2)], [], []], 0)
    assert cost[2] == math.inf
    assert path[2] is None


def test_matriz_no_es_simetrica_en_un_grafo_dirigido():
    D, paths = matriz_distancias(G, [0, 3])
    assert D == [[0, 4], [7, 0]]
    assert get_route(paths[1], 0) == [3, 0]


def test_el_grafo_de_surco_es_fuertemente_conexo(grafo):
    _, cost = dijkstra(grafo.G, 0)
    assert all(c < math.inf for c in cost)
