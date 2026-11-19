from app.graph import haversine, nodo_mas_cercano


def test_grafo_tiene_los_nodos_y_aristas_del_informe(grafo):
    assert grafo.num_nodos == 3854
    assert grafo.num_aristas == 9008


def test_indices_y_osmid_son_consistentes(grafo):
    for i in (0, 100, grafo.num_nodos - 1):
        assert grafo.w2i[grafo.labels[i]] == i


def test_pesos_son_positivos(grafo):
    assert all(w > 0 for adyacentes in grafo.G for _, w in adyacentes)


def test_nodo_mas_cercano_a_un_nodo_es_el_mismo(grafo):
    for i in (0, 1234, 3000):
        lon, lat = grafo.coords[i]
        cercano, distancia = nodo_mas_cercano(grafo, lon, lat)
        assert cercano == i
        assert distancia == 0


def test_haversine_un_grado_de_latitud_mide_unos_111_km():
    assert abs(haversine(-77.0, -12.0, -77.0, -13.0) - 111_195) < 50
