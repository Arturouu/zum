# Contrato de la API (el mismo que usa el frontend en frontend/src/types/ruta.ts).
# Todas las coordenadas van en orden [lon, lat], el que usa MapLibre.

from pydantic import BaseModel, Field

MAX_ENTREGAS = 10

LngLat = tuple[float, float]


class HealthResponse(BaseModel):
    status: str


class RouteRequest(BaseModel):
    """Cuerpo de POST /api/route."""

    origin: LngLat = Field(description="Punto de partida [lon, lat]")
    deliveries: list[LngLat] = Field(
        min_length=1, max_length=MAX_ENTREGAS, description="Entregas [lon, lat], de 1 a 10"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [{"origin": [-76.99, -12.14], "deliveries": [[-76.98, -12.15], [-77.0, -12.12]]}]
        }
    }


class Leg(BaseModel):
    """Un tramo de la ruta: el camino por calles entre dos paradas consecutivas."""

    coords: list[LngLat]
    distance_m: float


class RouteResponse(BaseModel):
    """Respuesta de POST /api/route."""

    order: list[int] = Field(
        description="Orden de visita. Empieza en 0 (el origen); deliveries[i] aparece como i + 1"
    )
    legs: list[Leg] = Field(description="Un tramo por entrega, en el orden de visita")
    total_distance_m: float
    exec_ms: float = Field(description="Tiempo de Dijkstra + backtracking, en milisegundos")
    states_explored: int = Field(description="Rutas parciales que exploró el backtracking")
