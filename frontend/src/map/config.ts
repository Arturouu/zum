import type { LngLatBoundsLike } from 'maplibre-gl'
import type { LngLat } from '../types/ruta'

// Estilos de OpenFreeMap (gratis, sin API key). "dark" se usa cuando el sistema está en modo oscuro.
export const ESTILO_CLARO = 'https://tiles.openfreemap.org/styles/liberty'
export const ESTILO_OSCURO = 'https://tiles.openfreemap.org/styles/dark'

export const CENTRO_SURCO: LngLat = [-76.99, -12.14]
export const ZOOM_INICIAL = 13
export const ZOOM_PUNTO = 15
export const ZOOM_MINIMO = 12

// Caja del polígono de Surco (-77.018, -12.174, -76.947, -12.076) con margen, para que el
// borde del distrito no quede pegado al filo y el mapa entre completo en pantallas anchas.
export const LIMITES_MAPA: LngLatBoundsLike = [
  [-77.09, -12.23],
  [-76.88, -12.02],
]
