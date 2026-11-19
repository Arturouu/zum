import pytest

from app.graph import cargar_grafo


@pytest.fixture(scope="session")
def grafo():
    """Grafo real de Surco, cargado una sola vez para todas las pruebas."""
    return cargar_grafo()
