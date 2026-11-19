# Generación del grafo vial de Santiago de Surco
#
# Este script documenta cómo se obtuvieron los archivos de esta carpeta. No hace falta
# ejecutarlo: los archivos ya están en el repositorio y, si se vuelve a correr, descarga
# los datos actuales de OpenStreetMap, que pueden no coincidir con los del informe.
#
#   surco_fc.graphml  grafo completo de OSMnx (incluye la geometría de cada calle)
#   nodos.csv         intersecciones: osmid, y (lat), x (lon), ...
#   aristas.csv       tramos de calle dirigidos: u, v, key, ..., oneway, length (metros), ...
#
# Pasos:
#  1. Se descarga la red para autos ("drive") de Santiago de Surco: las calles son aristas
#     y las intersecciones son nodos. Las calles de un solo sentido quedan como una sola
#     arista dirigida y las de doble sentido como dos (ida y vuelta): grafo dirigido.
#  2. Se conserva solo la componente fuertemente conexa más grande, para que desde
#     cualquier nodo se pueda llegar a cualquier otro respetando los sentidos de las calles.
#  3. Se guarda el grafo y se exportan los nodos y las aristas a CSV.
#
# Resultado: 3854 nodos y 9008 aristas.
#
# Uso (desde la carpeta dataset/, con el venv del backend activo):
#   python build_graph.py

import osmnx as ox

LUGAR = "Santiago de Surco, Lima, Peru"


# 1. Descargar la red vial
G = ox.graph_from_place(LUGAR, network_type="drive")

# 2. Componente fuertemente conexa más grande
G = ox.truncate.largest_component(G, strongly=True)
print("Nodos:", G.number_of_nodes())
print("Aristas:", G.number_of_edges())

# 3. Guardar el grafo y exportar los CSV
ox.save_graphml(G, "surco_fc.graphml")
nodos, aristas = ox.graph_to_gdfs(G)
nodos.drop(columns="geometry").to_csv("nodos.csv")
aristas.drop(columns="geometry").to_csv("aristas.csv")
print("Archivos guardados: surco_fc.graphml, nodos.csv y aristas.csv")
