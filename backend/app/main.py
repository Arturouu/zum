from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request

from .graph import cargar_grafo
from .schemas import HealthResponse, RouteRequest, RouteResponse

# Un punto marcado en el mapa se ubica en el nodo (intersección) más cercano. Dentro de
# Surco hay zonas sin calles para autos (parques, el aeródromo) donde la intersección más
# cercana queda a 300-400 m, así que el límite es holgado. Más lejos que esto, el punto
# está fuera de la red vial de Surco.
MAX_DISTANCIA_A_CALLE_M = 500


@asynccontextmanager
async def lifespan(app: FastAPI):
    # El grafo se carga una sola vez al iniciar el servidor (~40 ms) y se reutiliza
    app.state.grafo = cargar_grafo()
    yield


app = FastAPI(
    title="Zum API",
    description="Orden de entregas con la menor distancia total en Santiago de Surco.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/api/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.post("/api/route", response_model=RouteResponse)
def calcular_ruta(pedido: RouteRequest, request: Request) -> RouteResponse:
    """
    Calcula el orden de visita con la menor distancia total: sale del origen, pasa por
    todas las entregas y termina en la última (ruta abierta, no vuelve al origen).
    """
    # TODO(equipo): implementar con las funciones que ya están en graph.py, dijkstra.py
    # y tsp_backtracking.py. Pasos:
    #
    #  1. grafo = request.app.state.grafo
    #
    #  2. Ubicar cada punto en el grafo con nodo_mas_cercano(grafo, lon, lat), primero el
    #     origen y luego las entregas: puntos = [nodo_origen, nodo_entrega_1, ...].
    #     Si la distancia al nodo supera MAX_DISTANCIA_A_CALLE_M, responder
    #     HTTPException(422, "El punto ... está fuera de Surco o lejos de una calle").
    #
    #  3. inicio = time.perf_counter()
    #     D, paths = matriz_distancias(grafo.G, puntos)      # Dijkstra desde cada punto
    #     orden, total, estados = ruta_optima(D)             # backtracking con poda
    #     exec_ms = (time.perf_counter() - inicio) * 1000
    #
    #  4. Un tramo por cada par de paradas consecutivas (a, b) de `orden`:
    #       nodos = get_route(paths[a], puntos[b])           # camino calle por calle
    #       Leg(coords=[grafo.coords[i] for i in nodos], distance_m=D[a][b])
    #
    #  5. return RouteResponse(order=orden, legs=legs, total_distance_m=total,
    #                          exec_ms=exec_ms, states_explored=estados)
    #
    # Luego quitar el @pytest.mark.skip de tests/test_route.py y en el frontend crear
    # frontend/.env.local con VITE_USAR_MOCK=false para usar esta API en vez del mock.
    raise HTTPException(status_code=501, detail="POST /api/route todavía no está implementado.")
