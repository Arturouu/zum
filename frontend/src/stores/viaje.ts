import { reactive } from 'vue'
import type { LngLat, RouteResponse } from '../types/ruta'

// Estado compartido entre pantallas: lo que el usuario va marcando.
// Es un objeto reactivo simple (sin Pinia); cualquier vista lo importa y lo modifica.

export const MAX_ENTREGAS = 10

export interface Entrega {
  id: number
  coords: LngLat
}

export interface Aviso {
  tono: 'warning' | 'error' | 'success'
  texto: string
}

export const viaje = reactive({
  /** Punto de partida en [lon, lat]; null si todavía no se elige */
  origen: null as LngLat | null,
  /** Cómo se muestra el origen: "Tu ubicación" o "Punto en el mapa" */
  nombreOrigen: null as string | null,
  /** Entregas en el orden en que se agregaron (A, B, C…) */
  entregas: [] as Entrega[],
  /** Respuesta de POST /api/route, cuando ya se calculó */
  ruta: null as RouteResponse | null,
  /** Mensaje que la pantalla siguiente debe mostrar al entrar (p. ej. "fuera de Surco") */
  aviso: null as Aviso | null,
})

export function fijarOrigen(coords: LngLat, nombre: string) {
  viaje.origen = coords
  viaje.nombreOrigen = nombre
  viaje.ruta = null
}

export function quitarOrigen() {
  viaje.origen = null
  viaje.nombreOrigen = null
  viaje.ruta = null
}
