/** 4380 → "4.4 km", 850 → "850 m" */
export function formatearDistancia(metros: number): string {
  if (metros < 1000) return `${Math.round(metros)} m`
  return `${(metros / 1000).toFixed(1)} km`
}

/** 12.43 → "12 ms", 0.08 → "0.08 ms" */
export function formatearMs(ms: number): string {
  if (ms < 1) return `${ms.toFixed(2)} ms`
  return `${Math.round(ms)} ms`
}

/** 0 → "A", 1 → "B", … Letra con la que se marca cada entrega antes de calcular. */
export function letraEntrega(indice: number): string {
  return String.fromCharCode(65 + indice)
}
