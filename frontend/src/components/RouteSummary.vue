<script setup lang="ts">
import { computed } from 'vue'
import { formatearDistancia, formatearMs } from '../utils/formato'

// Distancia total y métricas del algoritmo (pantallas 05 y 08).
// Todas las cifras van en JetBrains Mono (.text-metric-*).
const props = withDefaults(
  defineProps<{
    distanciaTotalM: number
    execMs: number
    estadosExplorados: number
    /** Cuántas veces se ejecutó Dijkstra (una por origen + una por entrega) */
    ejecucionesDijkstra: number
    /** Texto junto a la distancia, p. ej. "4 entregas" o "Distancia total mínima" */
    detalle?: string
    /** Con caja de fondo, como en el panel de escritorio */
    enCaja?: boolean
  }>(),
  { detalle: '', enCaja: false },
)

const metricas = computed(() => [
  formatearMs(props.execMs),
  `${props.estadosExplorados} ${props.estadosExplorados === 1 ? 'estado' : 'estados'}`,
  `Dijkstra ×${props.ejecucionesDijkstra}`,
])
</script>

<template>
  <section class="resumen" :class="{ 'resumen--caja': props.enCaja }" aria-label="Resumen de la ruta">
    <p class="resumen__total">
      <span class="text-metric-lg">{{ formatearDistancia(props.distanciaTotalM) }}</span>
      <span v-if="props.detalle" class="resumen__detalle">{{ props.detalle }}</span>
    </p>
    <slot />
    <ul class="resumen__metricas" aria-label="Métricas del algoritmo">
      <li v-for="m in metricas" :key="m" class="chip text-metric-sm">{{ m }}</li>
    </ul>
  </section>
</template>

<style scoped>
.resumen {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.resumen--caja {
  padding: var(--space-4);
  border-radius: var(--radius-md);
  background: var(--bg-page);
}

.resumen__total {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 10px;
}

.resumen__detalle {
  font-size: 14px;
  line-height: 20px;
  font-weight: 500;
  color: var(--text-secondary);
}

.resumen__metricas {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  padding: 0;
  list-style: none;
}

.chip {
  padding: 6px 10px;
  border-radius: var(--radius-sm);
  background: var(--surface-sunken);
  color: var(--text-primary);
  font-variant-numeric: tabular-nums;
}

.resumen--caja .chip {
  border: 1px solid var(--border);
  background: var(--surface);
}
</style>
