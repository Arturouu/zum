import type { GeoJSONSource, Map as MapaLibre } from 'maplibre-gl'
import type { LngLat, RouteLeg } from '../types/ruta'
import { ANILLO_SURCO } from '../utils/geo'

// Capas propias que se dibujan sobre el estilo de OpenFreeMap.
// Hay que volver a agregarlas cada vez que cambia el estilo (evento "style.load").

const FUENTE_RUTA = 'ruta'

/** Lee un color de tokens.css para usarlo en una capa de MapLibre */
function token(nombre: string): string {
  return getComputedStyle(document.documentElement).getPropertyValue(nombre).trim()
}

/** Área con signo (fórmula del zapatero): sirve para saber el sentido de giro de un anillo */
function areaConSigno(anillo: LngLat[]): number {
  let suma = 0
  for (let i = 0, j = anillo.length - 1; i < anillo.length; j = i++) {
    suma += (anillo[j][0] - anillo[i][0]) * (anillo[j][1] + anillo[i][1])
  }
  return suma / 2
}

/**
 * Oscurece lo que está fuera de Santiago de Surco y marca el borde con una línea punteada.
 * El velo es un rectángulo enorme con el distrito como hueco (el hueco debe girar al revés).
 */
export function agregarLimiteSurco(mapa: MapaLibre, oscuro: boolean) {
  const exterior: LngLat[] = [
    [-78, -13],
    [-76, -13],
    [-76, -11],
    [-78, -11],
    [-78, -13],
  ]
  const hueco =
    Math.sign(areaConSigno(exterior)) === Math.sign(areaConSigno(ANILLO_SURCO))
      ? [...ANILLO_SURCO].reverse()
      : ANILLO_SURCO

  mapa.addSource('fuera-de-surco', {
    type: 'geojson',
    data: { type: 'Feature', properties: {}, geometry: { type: 'Polygon', coordinates: [exterior, hueco] } },
  })
  mapa.addLayer({
    id: 'fuera-de-surco',
    type: 'fill',
    source: 'fuera-de-surco',
    paint: { 'fill-color': token('--night-900'), 'fill-opacity': oscuro ? 0.35 : 0.12 },
  })

  mapa.addSource('limite-surco', {
    type: 'geojson',
    data: { type: 'Feature', properties: {}, geometry: { type: 'LineString', coordinates: ANILLO_SURCO } },
  })
  mapa.addLayer({
    id: 'limite-surco',
    type: 'line',
    source: 'limite-surco',
    layout: { 'line-join': 'round' },
    paint: { 'line-color': token('--text-secondary'), 'line-width': 2, 'line-dasharray': [3, 3] },
  })
}

/**
 * Fuente vacía + las dos capas de la ruta (handoff: "route-casing" abajo, "route" arriba).
 * Para dibujar una ruta, usar mostrarRuta().
 */
export function agregarCapasRuta(mapa: MapaLibre) {
  mapa.addSource(FUENTE_RUTA, { type: 'geojson', data: { type: 'FeatureCollection', features: [] } })
  mapa.addLayer({
    id: 'route-casing',
    type: 'line',
    source: FUENTE_RUTA,
    layout: { 'line-cap': 'round', 'line-join': 'round' },
    paint: { 'line-color': token('--route-casing'), 'line-width': 10 },
  })
  mapa.addLayer({
    id: 'route',
    type: 'line',
    source: FUENTE_RUTA,
    layout: { 'line-cap': 'round', 'line-join': 'round' },
    paint: { 'line-color': token('--brand'), 'line-width': 6 },
  })
}

/** Dibuja los tramos que devuelve POST /api/route (cada leg es una línea) */
export function mostrarRuta(mapa: MapaLibre, legs: RouteLeg[]) {
  mapa.getSource<GeoJSONSource>(FUENTE_RUTA)?.setData({
    type: 'FeatureCollection',
    features: legs.map((leg, i) => ({
      type: 'Feature',
      properties: { tramo: i + 1, distancia_m: leg.distance_m },
      geometry: { type: 'LineString', coordinates: leg.coords },
    })),
  })
}

export function limpiarRuta(mapa: MapaLibre) {
  mostrarRuta(mapa, [])
}
