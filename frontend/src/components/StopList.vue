<script setup lang="ts">
import { IconX } from '@tabler/icons-vue'
import { formatearDistancia } from '../utils/formato'
import StopMarker from './StopMarker.vue'

export interface Parada {
  id: number
  /** Letra (A, B, C…) antes de calcular o número de orden (1, 2, 3…) después */
  marcador: string
  titulo: string
  subtitulo?: string
  /** Distancia del tramo que llega a esta parada */
  distanciaM?: number
}

// Lista de paradas.
// - Con `quitable`: lista de entregas con botón para quitar (pantalla 04).
// - Con distancias y `origen`: orden de visita con la distancia de cada tramo (pantallas 06 y 08).
const props = withDefaults(
  defineProps<{
    paradas: Parada[]
    /** Si se pasa, agrega al inicio la fila del origen marcada como "Salida" */
    origen?: string
    quitable?: boolean
    /** Permite tocar una parada para resaltarla; emite "seleccionar" */
    seleccionable?: boolean
    seleccionada?: number | null
  }>(),
  { quitable: false, seleccionable: false, seleccionada: null },
)

const emit = defineEmits<{
  quitar: [id: number]
  seleccionar: [id: number]
}>()
</script>

<template>
  <ol class="lista">
    <li v-if="props.origen" class="parada">
      <span class="parada__origen" aria-hidden="true" />
      <span class="parada__texto">
        <span class="parada__titulo">{{ props.origen }}</span>
      </span>
      <span class="parada__salida">Salida</span>
    </li>

    <li
      v-for="p in props.paradas"
      :key="p.id"
      class="parada"
      :class="{ 'parada--seleccionada': p.id === props.seleccionada, 'parada--seleccionable': props.seleccionable }"
      :aria-current="p.id === props.seleccionada ? 'step' : undefined"
      :tabindex="props.seleccionable ? 0 : undefined"
      @click="props.seleccionable && emit('seleccionar', p.id)"
      @keydown.enter="props.seleccionable && emit('seleccionar', p.id)"
    >
      <StopMarker :etiqueta="p.marcador" />
      <span class="parada__texto">
        <span class="parada__titulo">{{ p.titulo }}</span>
        <span v-if="p.subtitulo" class="parada__subtitulo">{{ p.subtitulo }}</span>
      </span>
      <span v-if="p.distanciaM !== undefined" class="parada__distancia text-metric-sm">
        {{ formatearDistancia(p.distanciaM) }}
      </span>
      <button
        v-if="props.quitable"
        type="button"
        class="parada__quitar"
        :aria-label="`Quitar ${p.titulo}`"
        @click.stop="emit('quitar', p.id)"
      >
        <IconX :size="22" aria-hidden="true" />
      </button>
    </li>
  </ol>
</template>

<style scoped>
.lista {
  padding: 0;
  list-style: none;
}

.parada {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  min-height: 52px;
  padding: var(--space-1) 0;
  border-bottom: 1px solid var(--border);
}

.parada--seleccionable {
  cursor: pointer;
}

.parada:last-child {
  border-bottom: 0;
}

.parada--seleccionada {
  margin: 0 calc(-1 * var(--space-2));
  padding: var(--space-1) var(--space-2);
  border-bottom-color: transparent;
  border-radius: var(--radius-md);
  background: var(--brand-tint);
}

.parada__texto {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-width: 0;
}

.parada__titulo {
  font-size: 16px;
  line-height: 24px;
  font-weight: 600;
}

.parada__subtitulo {
  font-size: 14px;
  line-height: 20px;
  color: var(--text-secondary);
}

.parada__distancia {
  color: var(--text-secondary);
  font-variant-numeric: tabular-nums;
}

.parada--seleccionada .parada__distancia {
  color: var(--text-brand);
}

.parada__salida {
  font-size: 14px;
  line-height: 20px;
  color: var(--text-secondary);
}

.parada__origen {
  flex: none;
  width: 14px;
  height: 14px;
  margin: 0 7px;
  border-radius: var(--radius-full);
  background: var(--location);
  box-shadow:
    0 0 0 3px var(--surface),
    0 0 0 6px var(--location-halo);
}

.parada__quitar {
  display: flex;
  flex: none;
  align-items: center;
  justify-content: center;
  width: var(--hit-target);
  height: var(--hit-target);
  padding: 0;
  border: 0;
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--text-secondary);
}

.parada__quitar:hover {
  background: var(--bg-danger);
  color: var(--text-danger);
}
</style>
