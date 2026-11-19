import type { LngLat, RouteLeg, RouteRequest, RouteResponse } from '../types/ruta'
import { distanciaRecta } from '../utils/geo'

/**
 * Mientras el backend no tenga POST /api/route se usa un mock con la misma forma.
 * Para usar el backend real, crear frontend/.env.local con:  VITE_USAR_MOCK=false
 */
const USAR_MOCK = import.meta.env.VITE_USAR_MOCK !== 'false'

/** Calcula el orden de visita con la menor distancia total (POST /api/route). */
export function calcularRuta(pedido: RouteRequest): Promise<RouteResponse> {
  return USAR_MOCK ? calcularRutaMock(pedido) : calcularRutaApi(pedido)
}

// ---------- Llamada real ----------

async function calcularRutaApi(pedido: RouteRequest): Promise<RouteResponse> {
  const res = await fetch('/api/route', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(pedido),
  })
  if (!res.ok) {
    // FastAPI responde los errores como { "detail": ... }
    const cuerpo = await res.json().catch(() => null)
    const detalle = typeof cuerpo?.detail === 'string' ? cuerpo.detail : `Error ${res.status}`
    throw new Error(`No se pudo calcular la ruta: ${detalle}`)
  }
  return res.json()
}

// ---------- Mock ----------

// Factor para que la línea recta se parezca a una distancia por calles
const FACTOR_CALLES = 1.3

/**
 * NO es el algoritmo de Zum: elige siempre la entrega más cercana (vecino más cercano)
 * y une las paradas con líneas rectas. Solo sirve para probar la interfaz.
 */
async function calcularRutaMock({ origin, deliveries }: RouteRequest): Promise<RouteResponse> {
  const inicio = performance.now()
  const puntos: LngLat[] = [origin, ...deliveries]
  const pendientes = new Set(deliveries.map((_, i) => i + 1))
  const order = [0]
  const legs: RouteLeg[] = []

  let actual = 0
  while (pendientes.size > 0) {
    let siguiente = -1
    let mejor = Infinity
    for (const j of pendientes) {
      const d = distanciaRecta(puntos[actual], puntos[j])
      if (d < mejor) {
        mejor = d
        siguiente = j
      }
    }
    pendientes.delete(siguiente)
    order.push(siguiente)
    legs.push({ coords: [puntos[actual], puntos[siguiente]], distance_m: Math.round(mejor * FACTOR_CALLES) })
    actual = siguiente
  }

  const execMs = +(performance.now() - inicio).toFixed(2)
  await new Promise((r) => setTimeout(r, 600)) // simula la espera del servidor

  return {
    order,
    legs,
    total_distance_m: legs.reduce((suma, leg) => suma + leg.distance_m, 0),
    exec_ms: execMs,
    states_explored: deliveries.length * (deliveries.length + 1) / 2,
  }
}
