// Tipos del contrato con el backend (POST /api/route).
// Todas las coordenadas van en orden [lon, lat], el mismo que usa MapLibre.

export type LngLat = [number, number]

/** Cuerpo de POST /api/route. Entre 1 y 10 entregas. */
export interface RouteRequest {
  origin: LngLat
  deliveries: LngLat[]
}

/** Un tramo de la ruta: el camino por calles entre dos paradas consecutivas. */
export interface RouteLeg {
  coords: LngLat[]
  distance_m: number
}

/** Respuesta de POST /api/route. */
export interface RouteResponse {
  /**
   * Orden óptimo de visita. Empieza en 0 (el origen); la entrega `deliveries[i]` del
   * request aparece como `i + 1`. Ej.: [0, 2, 1] = origen → 2.ª entrega → 1.ª entrega.
   */
  order: number[]
  /** Un tramo por entrega, en el mismo orden que `order`. La ruta es abierta: no vuelve al origen. */
  legs: RouteLeg[]
  total_distance_m: number
  exec_ms: number
  states_explored: number
}
