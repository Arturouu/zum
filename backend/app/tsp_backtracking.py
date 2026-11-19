# Orden de visita con la menor distancia total - Técnica: Backtracking con poda
#
# Sustento:
#  - Es una variante del problema del viajante (TSP) con ruta abierta: se sale del origen
#    (punto 0), se visita cada entrega una sola vez y se termina en la última entrega,
#    sin volver al origen.
#  - Las distancias entre puntos salen de la matriz D que arma Dijkstra (ver dijkstra.py).
#    D no es simétrica porque el grafo es dirigido (calles de un solo sentido).
#  - Se arma el orden de visita parada por parada. En cada nivel se prueba cada entrega
#    que aún no se visitó; cuando ya están todas, se compara con la mejor ruta encontrada.
#    Luego se quita la última parada (retroceder) para probar la siguiente opción.
#  - Poda: si la distancia acumulada de una ruta parcial ya es mayor o igual que la mejor
#    ruta completa conocida, se descarta, porque sumar más tramos nunca la reduce (todas
#    las distancias son positivas).
#  - Para podar antes, en cada nivel se prueban primero las entregas más cercanas: así se
#    encuentra pronto una ruta buena y se descartan más ramas.
#  - Peor caso: se recorren todas las permutaciones, O(n!). Con 10 entregas son
#    10! = 3 628 800 rutas; la poda deja los estados explorados muy por debajo de eso.


import math


def ruta_optima(D: list[list[float]]) -> tuple[list[int], float, int]:
    """
    D[i][j]: distancia del punto i al punto j (0 = origen, 1..n = entregas).
    Devuelve (orden, distancia_total, estados_explorados):
      orden               índices de los puntos en el orden de visita, empieza en 0
      distancia_total     suma de los tramos de ese orden (sin volver al origen)
      estados_explorados  cuántas rutas parciales se generaron (llamadas a backtracking)
    """
    n = len(D)
    mejor_orden = []
    mejor_distancia = math.inf
    estados = 0

    def backtracking(actual, recorrido, visitados, acumulado):
        nonlocal mejor_orden, mejor_distancia, estados
        estados += 1

        # Caso 1: Poda. Esta ruta parcial ya no puede mejorar a la mejor conocida
        if acumulado >= mejor_distancia:
            return

        # Caso 2: Se visitaron todas las entregas. Es la mejor ruta hasta ahora
        # (si no lo fuera, la poda la habría descartado)
        if len(recorrido) == n:
            mejor_distancia = acumulado
            mejor_orden = recorrido[:]
            return

        # Opción: Probar cada entrega no visitada como siguiente parada, la más cercana primero
        candidatos = sorted((j for j in range(1, n) if not visitados[j]), key=lambda j: D[actual][j])
        for siguiente in candidatos:
            visitados[siguiente] = True
            recorrido.append(siguiente)
            backtracking(siguiente, recorrido, visitados, acumulado + D[actual][siguiente])

            # Backtracking: Quitar la parada para probar con otra entrega
            recorrido.pop()
            visitados[siguiente] = False

    visitados = [False] * n
    visitados[0] = True
    backtracking(0, [0], visitados, 0)
    return mejor_orden, mejor_distancia, estados
