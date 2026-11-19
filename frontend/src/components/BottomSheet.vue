<script setup lang="ts">
// Contenedor del contenido de la vista del mapa.
// En celular es una hoja inferior con agarre; desde 768 px el mismo contenido
// se muestra como panel lateral (<aside>) de --sidebar-width a la izquierda del mapa.
const props = defineProps<{
  /** Nombre accesible del panel */
  etiqueta: string
}>()
</script>

<template>
  <aside class="hoja" :aria-label="props.etiqueta">
    <span class="hoja__agarre" aria-hidden="true" />
    <div class="hoja__contenido">
      <slot />
    </div>
  </aside>
</template>

<style scoped>
.hoja {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  max-height: 70dvh;
  padding: var(--space-3) var(--space-4) calc(var(--space-5) + env(safe-area-inset-bottom));
  border-radius: var(--radius-sheet) var(--radius-sheet) 0 0;
  background: var(--surface);
  box-shadow: var(--shadow-sheet);
  pointer-events: auto;
}

.hoja__agarre {
  flex: none;
  align-self: center;
  width: 40px;
  height: 4px;
  border-radius: var(--radius-full);
  background: var(--border-strong);
}

.hoja__contenido {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  min-height: 0;
  overflow-y: auto;
}

@media (min-width: 768px) {
  .hoja {
    width: var(--sidebar-width);
    height: 100%;
    max-height: none;
    padding: var(--space-5);
    border-radius: 0;
    border-right: 1px solid var(--border);
    box-shadow: none;
  }

  .hoja__agarre {
    display: none;
  }

  .hoja__contenido {
    flex: 1;
    gap: 20px;
  }
}
</style>
