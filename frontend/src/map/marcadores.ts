import { Marker } from 'maplibre-gl'
import { createApp } from 'vue'
import StopMarker from '../components/StopMarker.vue'
import type { LngLat } from '../types/ruta'
import './marcadores.css'

/** Punto cian del origen (18 px, borde blanco y halo). Se puede arrastrar. */
export function crearMarcadorOrigen(coords: LngLat): Marker {
  const el = document.createElement('div')
  el.className = 'marcador-origen'
  el.setAttribute('role', 'img')
  el.setAttribute('aria-label', 'Punto de partida')
  return new Marker({ element: el, draggable: true }).setLngLat(coords)
}

/**
 * Marcador de parada: StopMarker con letra (A, B, C…) antes de calcular
 * o número (1, 2, 3…) en el orden óptimo después.
 * Con `seleccionada` se le agrega el halo de la parada resaltada (pantalla 06).
 *
 *   crearMarcadorParada('A', [-76.99, -12.14]).addTo(mapa)
 */
export function crearMarcadorParada(etiqueta: string, coords: LngLat, seleccionada = false): Marker {
  const el = document.createElement('div')
  el.setAttribute('role', 'img')
  el.setAttribute('aria-label', `Parada ${etiqueta}`)
  const app = createApp(StopMarker, { etiqueta, enMapa: true, seleccionada })
  app.mount(el)

  const marcador = new Marker({ element: el }).setLngLat(coords)
  // Al quitar el marcador también se desmonta el componente de Vue
  const quitar = marcador.remove.bind(marcador)
  marcador.remove = () => {
    app.unmount()
    return quitar()
  }
  return marcador
}
