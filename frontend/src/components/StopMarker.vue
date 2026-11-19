<script setup lang="ts">
// Marcador de parada: círculo invertido con la letra (antes de calcular) o el número (después).
// Se usa en StopList y, montado como elemento HTML, en el mapa (ver src/map/marcadores.ts).
const props = withDefaults(
  defineProps<{
    etiqueta: string
    seleccionada?: boolean
    /** En el mapa lleva borde blanco para separarse de las calles */
    enMapa?: boolean
  }>(),
  { seleccionada: false, enMapa: false },
)
</script>

<template>
  <span
    class="stop-marker"
    :class="{ 'stop-marker--seleccionada': props.seleccionada, 'stop-marker--mapa': props.enMapa }"
    aria-hidden="true"
  >
    {{ props.etiqueta }}
  </span>
</template>

<style scoped>
.stop-marker {
  display: inline-flex;
  flex: none;
  align-items: center;
  justify-content: center;
  width: var(--marker-stop);
  height: var(--marker-stop);
  border-radius: var(--radius-full);
  background: var(--surface-inverse);
  color: var(--text-on-inverse);
  font-family: var(--font-sans);
  font-size: 14px;
  line-height: 1;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
}

.stop-marker--mapa {
  box-shadow:
    0 0 0 2px var(--surface),
    var(--shadow-control);
}

.stop-marker--seleccionada {
  box-shadow:
    0 0 0 2px var(--surface),
    0 0 0 8px color-mix(in srgb, var(--brand) 25%, transparent);
}
</style>
