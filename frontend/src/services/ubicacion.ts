import type { LngLat } from '../types/ruta'

/**
 * Pide la ubicación del dispositivo y la devuelve en [lon, lat].
 * Ojo: el navegador solo la da en https o en localhost; si se abre la app desde
 * el celular por la IP de la red local (http://192.168…), falla con permiso denegado.
 */
export function obtenerUbicacion(): Promise<LngLat> {
  return new Promise((resolve, reject) => {
    if (!('geolocation' in navigator)) {
      reject(new Error('Tu navegador no permite obtener la ubicación.'))
      return
    }
    navigator.geolocation.getCurrentPosition(
      (pos) => resolve([pos.coords.longitude, pos.coords.latitude]),
      (err) => {
        const mensajes: Record<number, string> = {
          [err.PERMISSION_DENIED]: 'No diste permiso para usar tu ubicación.',
          [err.POSITION_UNAVAILABLE]: 'No pudimos saber dónde estás.',
          [err.TIMEOUT]: 'Tu ubicación tardó demasiado en llegar.',
        }
        reject(new Error(mensajes[err.code] ?? 'No pudimos obtener tu ubicación.'))
      },
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 },
    )
  })
}
