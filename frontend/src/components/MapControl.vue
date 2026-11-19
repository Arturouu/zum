<script setup lang="ts">
// Botón circular que flota sobre el mapa. `etiqueta` es obligatoria porque solo muestra un ícono.
const props = withDefaults(
  defineProps<{
    etiqueta: string
    /** "info" pinta el ícono cian (ubicación) */
    tono?: 'neutro' | 'info'
  }>(),
  { tono: 'neutro' },
)
</script>

<template>
  <button
    type="button"
    class="map-control"
    :class="`map-control--${props.tono}`"
    :aria-label="props.etiqueta"
    :title="props.etiqueta"
  >
    <slot />
  </button>
</template>

<style scoped>
.map-control {
  display: flex;
  align-items: center;
  justify-content: center;
  width: var(--map-control);
  height: var(--map-control);
  padding: 0;
  border: 0;
  border-radius: var(--radius-full);
  background: var(--surface-raised);
  color: var(--text-primary);
  box-shadow: var(--shadow-control);
  pointer-events: auto;
}

.map-control--info {
  color: var(--text-info);
}

.map-control:hover {
  background: var(--surface-sunken);
}
</style>
