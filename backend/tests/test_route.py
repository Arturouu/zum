import pytest
from fastapi.testclient import TestClient

from app.main import app

ORIGEN = [-76.99, -12.14]
# Puntos de Surco a menos de 250 m de una intersección
ENTREGAS = [[-76.975, -12.13], [-76.995, -12.11], [-76.985, -12.142]]


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


# ---------- Validación del contrato (ya funciona) ----------


def test_rechaza_sin_entregas(client):
    respuesta = client.post("/api/route", json={"origin": ORIGEN, "deliveries": []})
    assert respuesta.status_code == 422


def test_rechaza_mas_de_10_entregas(client):
    respuesta = client.post("/api/route", json={"origin": ORIGEN, "deliveries": [ENTREGAS[0]] * 11})
    assert respuesta.status_code == 422


def test_rechaza_coordenadas_mal_formadas(client):
    respuesta = client.post("/api/route", json={"origin": [-76.99], "deliveries": ENTREGAS})
    assert respuesta.status_code == 422


# ---------- Cálculo de la ruta: TODO(equipo) ----------
# Quitar el skip cuando POST /api/route esté implementado (ver app/main.py).

pendiente = pytest.mark.skip(reason="TODO(equipo): implementar POST /api/route")


@pendiente
def test_devuelve_una_ruta_valida(client):
    respuesta = client.post("/api/route", json={"origin": ORIGEN, "deliveries": ENTREGAS})
    assert respuesta.status_code == 200
    ruta = respuesta.json()

    # El orden empieza en el origen y visita cada entrega una sola vez
    assert ruta["order"][0] == 0
    assert sorted(ruta["order"]) == list(range(len(ENTREGAS) + 1))

    # Un tramo por entrega; la distancia total es la suma de los tramos
    assert len(ruta["legs"]) == len(ENTREGAS)
    assert ruta["total_distance_m"] == pytest.approx(sum(leg["distance_m"] for leg in ruta["legs"]))

    # Cada tramo empieza donde terminó el anterior
    for anterior, siguiente in zip(ruta["legs"], ruta["legs"][1:]):
        assert anterior["coords"][-1] == siguiente["coords"][0]

    assert ruta["exec_ms"] >= 0
    assert ruta["states_explored"] > 0


@pendiente
def test_una_sola_entrega(client):
    respuesta = client.post("/api/route", json={"origin": ORIGEN, "deliveries": [ENTREGAS[0]]})
    assert respuesta.status_code == 200
    assert respuesta.json()["order"] == [0, 1]


@pendiente
def test_rechaza_un_punto_fuera_de_surco(client):
    miraflores = [-77.03, -12.12]
    respuesta = client.post("/api/route", json={"origin": ORIGEN, "deliveries": [miraflores]})
    assert respuesta.status_code == 422
