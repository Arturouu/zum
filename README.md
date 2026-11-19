# Zum

Zum calcula el **orden de visita con la menor distancia total** para un reparto en Santiago de Surco (Lima). El usuario marca un punto de partida y hasta 10 entregas en el mapa, y Zum devuelve en qué orden visitarlas y la ruta calle por calle.

Trabajo Final de Complejidad Algorítmica (1ACC0184, UPC 2026-2).

- **Grafo:** red vial de Surco tomada de OpenStreetMap con OSMnx. Es dirigido, ponderado por distancia (`length`, en metros) y fuertemente conexo: 3854 nodos y 9008 aristas.
- **Algoritmos:** Dijkstra desde el origen y desde cada entrega arma la matriz de distancias; luego un backtracking con poda encuentra el orden óptimo. La ruta es abierta: termina en la última entrega, sin volver al origen.

## Stack

| Parte | Tecnologías |
|---|---|
| Frontend | Vue 3, Vite, TypeScript, vue-router, MapLibre GL JS (estilo de OpenFreeMap), @tabler/icons-vue |
| Backend | Python 3.11+, FastAPI, Uvicorn, Pydantic, OSMnx, scikit-learn, pytest |

## Estructura

```
zum/
├── backend/            API en FastAPI (app/) y pruebas (tests/)
├── dataset/            Grafo de Surco y el script que documenta cómo se generó
├── docs/design/        Handoff de diseño: PNG de cada pantalla, tokens.css, logos
└── frontend/
    └── src/
        ├── components/ Componentes del design system (ver docs/design/HANDOFF.md)
        ├── map/        Configuración de MapLibre, capas, marcadores y límite de Surco
        ├── services/   route.ts (POST /api/route, con mock) y ubicacion.ts
        ├── stores/     viaje.ts: origen, entregas y ruta compartidos entre pantallas
        ├── styles/     tokens.css (colores, espaciado, tipografía) y estilos base
        ├── types/      Tipos del contrato con el backend
        ├── utils/      Formato de distancias y geometría (punto dentro de Surco)
        └── views/      Bienvenida (/), Punto de partida (/inicio) y MapView (/mapa)
```

## Cómo correrlo

### Frontend

Requiere Node 20.19 o superior (o Node 22.12+).

```bash
cd frontend
npm install
npm run dev
```

Abre <http://localhost:5173>. Para el build de producción: `npm run build`.

Para probarlo en el celular dentro de la misma red: `npm run dev -- --host` y abrir la IP que muestra Vite. Ojo: el navegador solo da la ubicación en `https` o en `localhost`, así que desde el celular hay que usar **Elegir en el mapa**.

### Backend

> Todavía es un esqueleto: el grafo, Dijkstra y el backtracking se agregan en la rama `feature/backend-grafo`.

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows  (en macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
uvicorn app.main:app --reload
```

La API queda en <http://localhost:8000>. Vite redirige las llamadas a `/api` hacia ese puerto.

Mientras el backend no tenga `POST /api/route`, el frontend usa un **mock** (`frontend/src/services/route.ts`). Para usar el backend real, crear `frontend/.env.local` con:

```
VITE_USAR_MOCK=false
```

## Contrato de la API

`POST /api/route` (coordenadas siempre en orden `[lon, lat]`):

```json
{ "origin": [-76.99, -12.14], "deliveries": [[-76.98, -12.15], [-77.00, -12.12]] }
```

```json
{ "order": [0, 2, 1],
  "legs": [{ "coords": [[-76.99, -12.14], [-76.985, -12.145]], "distance_m": 1840 }],
  "total_distance_m": 5230, "exec_ms": 12.4, "states_explored": 37 }
```

- `order` empieza en `0` (el origen); la entrega `deliveries[i]` aparece como `i + 1`.
- `legs` tiene un tramo por entrega, en el orden de `order`.

Los tipos están en `frontend/src/types/ruta.ts`.

## Qué está hecho y qué falta

**Hecho**

- Pantallas 01/09 (bienvenida), 02 (punto de partida) y 03 (mapa sin entregas), en celular y escritorio.
- Origen: con la ubicación del dispositivo o tocando el mapa; se puede arrastrar. Si el punto cae fuera de Surco, se avisa.
- Mapa limitado a Surco, con el borde del distrito y modo oscuro según el sistema.
- Todos los componentes del handoff, el mock de `POST /api/route` y los helpers del mapa.

**Falta (pantallas 04 a 06)**, en `frontend/src/views/MapView.vue`, marcado con `TODO(equipo)`:

1. **Agregar entregas** (pantalla 04) en `alTocarMapa()`: guardar en `viaje.entregas`, dibujar `crearMarcadorParada(letraEntrega(i), punto)`, máximo `MAX_ENTREGAS` (10), y listarlas con `<StopList quitable>`.
2. **Calcular la ruta** (pantalla 05) en `calcular()`: llamar a `calcularRuta()`, guardar la respuesta en `viaje.ruta`, dibujarla con `mostrarRuta(mapa, legs)`, renumerar las paradas según `order` y mostrar `<RouteSummary>`.
3. **Ver pasos** (pantalla 06): `<StopList>` con `origen`, distancias por tramo y la parada seleccionada resaltada.
4. **Backend:** implementar `POST /api/route` con Dijkstra y el backtracking.

El diseño de cada pantalla está en `docs/design/png/` y las reglas en `docs/design/HANDOFF.md`.

## Flujo de trabajo

- Ramas `feature/<nombre>` creadas desde `develop`.
- Commits con [Conventional Commits](https://www.conventionalcommits.org/es/): `feat(frontend): …`, `fix(backend): …`, `docs: …`.

## Datos

Mapa y red vial © colaboradores de [OpenStreetMap](https://www.openstreetmap.org/copyright) (ODbL). Teselas de [OpenFreeMap](https://openfreemap.org).
