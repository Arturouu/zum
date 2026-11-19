# Zum

Zum is a delivery routing web application for Santiago de Surco (Lima, Peru). The user marks a starting point and up to 10 delivery stops on the map, and Zum returns the visiting order with the **shortest total distance**, drawn street by street. The road network is a directed, weighted graph built from OpenStreetMap (3,854 nodes and 9,008 edges, weighted by length in meters). Dijkstra's algorithm, run from the origin and from each stop, builds the distance matrix, and a backtracking search with pruning finds the optimal order. The route is open: it ends at the last delivery and does not return to the origin.

Final project for the Algorithmic Complexity course (1ACC0184) at UPC, 2026-2.

## Tech Stack

- **Frontend:** Vue 3, Vite, TypeScript, Vue Router
- **Maps:** MapLibre GL JS with OpenFreeMap tiles
- **Icons:** Tabler Icons (`@tabler/icons-vue`)
- **Backend:** Python 3.11+, FastAPI, Uvicorn, Pydantic
- **Graph:** OSMnx (graph loading and nearest node lookup), scikit-learn
- **Testing:** pytest, httpx

## Prerequisites

- Node.js 20.19+ (or 22.12+)
- Python 3.11+

## Project Structure

```text
zum/
├── backend/
│   ├── app/                # FastAPI app, graph loading, Dijkstra, backtracking, schemas
│   └── tests/              # pytest tests
├── dataset/                # Santiago de Surco road graph and the script that documents how it was built
└── frontend/
    └── src/
        ├── components/     # Design system components
        ├── map/            # MapLibre config, layers, markers, Surco boundary
        ├── services/       # API calls (route.ts) and geolocation
        ├── stores/         # Shared trip state (origin, deliveries, route)
        ├── styles/         # Design tokens and base styles
        ├── types/          # API contract types
        ├── utils/          # Formatting and geometry helpers
        └── views/          # Welcome (/), Starting point (/inicio), Map (/mapa)
```

## Configuration

- **API proxy:** in development, Vite forwards every `/api` request to `http://localhost:8000` (`frontend/vite.config.ts`).
- **Route mock:** by default the frontend answers `POST /api/route` with a mock in `frontend/src/services/route.ts`. To use the real backend, create `frontend/.env.local` with:

  ```bash
  VITE_USAR_MOCK=false
  ```

## Getting Started

### 1) Backend

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000`. The interactive docs are at `http://localhost:8000/docs`.

### 2) Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

To try it on a phone on the same network, run `npm run dev -- --host` and open the network URL Vite prints. Browsers only share the device location over HTTPS or `localhost`, so on the phone use **Elegir en el mapa** to pick the starting point.

## Scripts and Commands

- `npm run dev`: Start the frontend dev server.
- `npm run build`: Type-check and build the frontend for production.
- `npm run preview`: Serve the production build locally.
- `uvicorn app.main:app --reload`: Start the backend.
- `pytest`: Run the backend tests (from `backend/`).

## API Surface

- `GET /api/health`: Health check. Returns `{ "status": "ok" }`.
- `POST /api/route`: Computes the visiting order with the shortest total distance.

Coordinates are always `[lon, lat]`. Request (1 to 10 deliveries):

```json
{ "origin": [-76.99, -12.14], "deliveries": [[-76.98, -12.15], [-77.00, -12.12]] }
```

Response:

```json
{
  "order": [0, 2, 1],
  "legs": [{ "coords": [[-76.99, -12.14], [-76.985, -12.145]], "distance_m": 1840 }],
  "total_distance_m": 5230,
  "exec_ms": 12.4,
  "states_explored": 37
}
```

- `order` starts with `0` (the origin); `deliveries[i]` appears as `i + 1`.
- `legs` has one leg per delivery, in visiting order.

The TypeScript types live in `frontend/src/types/ruta.ts`.

## Development Conventions

- **Branches:** `feature/<name>` branches created from `develop`.
- **Commits:** [Conventional Commits](https://www.conventionalcommits.org/) written in English, e.g. `feat(frontend): ...`, `fix(backend): ...`, `docs: ...`.
- **Design:** colors, spacing, radii and typography come only from `frontend/src/styles/tokens.css`.
- **Distance only:** routes are optimized by distance (`length` in meters), never by time or traffic, and respect one-way streets.

## Data Sources

Map data and road network © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors (ODbL). Map tiles by [OpenFreeMap](https://openfreemap.org).
