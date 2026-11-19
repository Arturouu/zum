import limiteSurco from '../map/surco-limite.json'
import type { LngLat } from '../types/ruta'

/** Anillo exterior del polígono de Santiago de Surco, en [lon, lat] */
export const ANILLO_SURCO = limiteSurco.geometry.coordinates[0] as LngLat[]

/**
 * Ray casting: se traza una semirrecta horizontal desde el punto y se cuentan los cruces
 * con los lados del polígono. Un número impar de cruces significa que el punto está dentro.
 */
export function puntoEnPoligono([x, y]: LngLat, anillo: LngLat[]): boolean {
  let dentro = false
  for (let i = 0, j = anillo.length - 1; i < anillo.length; j = i++) {
    const [xi, yi] = anillo[i]
    const [xj, yj] = anillo[j]
    const cruza = yi > y !== yj > y && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi
    if (cruza) dentro = !dentro
  }
  return dentro
}

/** ¿El punto está dentro del distrito? Se usa para el origen y para cada entrega. */
export function estaDentroDeSurco(punto: LngLat): boolean {
  return puntoEnPoligono(punto, ANILLO_SURCO)
}

/** Distancia en línea recta (haversine), en metros. Solo para el mock y estimaciones. */
export function distanciaRecta([lon1, lat1]: LngLat, [lon2, lat2]: LngLat): number {
  const R = 6371000
  const rad = Math.PI / 180
  const dLat = (lat2 - lat1) * rad
  const dLon = (lon2 - lon1) * rad
  const a = Math.sin(dLat / 2) ** 2 + Math.cos(lat1 * rad) * Math.cos(lat2 * rad) * Math.sin(dLon / 2) ** 2
  return 2 * R * Math.asin(Math.sqrt(a))
}
