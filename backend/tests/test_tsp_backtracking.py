import itertools
import math
import random

from app.dijkstra import matriz_distancias
from app.tsp_backtracking import ruta_optima


def fuerza_bruta(D):
    """Prueba todas las permutaciones de entregas: sirve para comprobar el backtracking."""
    mejor = math.inf
    for p in itertools.permutations(range(1, len(D))):
        orden = (0,) + p
        mejor = min(mejor, sum(D[a][b] for a, b in zip(orden, orden[1:])))
    return mejor


def distancia_de(D, orden):
    return sum(D[a][b] for a, b in zip(orden, orden[1:]))


def test_matriz_pequena_con_respuesta_conocida():
    # Desde 0 conviene ir a 2, luego a 1 y terminar en 3: 1 + 1 + 1 = 3
    D = [
        [0, 5, 1, 9],
        [5, 0, 1, 1],
        [1, 1, 0, 8],
        [9, 1, 8, 0],
    ]
    orden, distancia, estados = ruta_optima(D)
    assert orden == [0, 2, 1, 3]
    assert distancia == 3
    assert estados > 0


def test_ruta_abierta_no_suma_la_vuelta_al_origen():
    # Volver al origen desde 2 cuesta 100, pero no debe contarse
    D = [
        [0, 1, 50],
        [50, 0, 1],
        [100, 50, 0],
    ]
    orden, distancia, _ = ruta_optima(D)
    assert orden == [0, 1, 2]
    assert distancia == 2


def test_respeta_la_asimetria():
    # Ir de 1 a 2 es barato, de 2 a 1 es caro
    D = [
        [0, 3, 3],
        [3, 0, 1],
        [3, 20, 0],
    ]
    orden, distancia, _ = ruta_optima(D)
    assert orden == [0, 1, 2]
    assert distancia == 4


def test_una_sola_entrega():
    orden, distancia, _ = ruta_optima([[0, 7], [7, 0]])
    assert orden == [0, 1]
    assert distancia == 7


def test_coincide_con_fuerza_bruta_en_matrices_aleatorias():
    random.seed(1)
    for n in range(1, 8):
        for _ in range(10):
            D = [[0 if i == j else random.randint(1, 100) for j in range(n + 1)] for i in range(n + 1)]
            orden, distancia, _ = ruta_optima(D)
            assert sorted(orden) == list(range(n + 1)) and orden[0] == 0
            assert distancia == distancia_de(D, orden) == fuerza_bruta(D)


def test_la_poda_explora_menos_estados_que_todas_las_rutas_parciales():
    # Sin poda, el árbol de búsqueda de 8 entregas tiene sum(8!/(8-k)!) = 109 601 nodos
    random.seed(2)
    D = [[0 if i == j else random.randint(1, 100) for j in range(9)] for i in range(9)]
    _, _, estados = ruta_optima(D)
    assert estados < 109_601


def test_con_10_entregas_del_grafo_de_surco(grafo):
    random.seed(3)
    puntos = random.sample(range(grafo.num_nodos), 11)
    D, _ = matriz_distancias(grafo.G, puntos)
    orden, distancia, _ = ruta_optima(D)
    assert len(orden) == 11 and orden[0] == 0
    assert math.isclose(distancia, distancia_de(D, orden))
