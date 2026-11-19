<script setup lang="ts">
import { IconArrowRight, IconMapPin, IconPencil } from '@tabler/icons-vue'
import { computed } from 'vue'

// Origen (punto cian) y resumen de entregas.
// - Normal: tarjeta flotante sobre el mapa (pantallas 03 y 04).
// - `plano`: sin tarjeta, dentro del panel lateral de escritorio (pantalla 08).
// - `compacto`: una sola línea "origen → N entregas" con botón de editar (pantalla 05).
const props = withDefaults(
  defineProps<{
    /** Nombre del origen ("Tu ubicación", "Punto en el mapa") o null si aún no se elige */
    origen: string | null
    /** Letras de las entregas marcadas, en el orden en que se agregaron */
    entregas?: string[]
    plano?: boolean
    compacto?: boolean
  }>(),
  { entregas: () => [], plano: false, compacto: false },
)

const emit = defineEmits<{ editar: [] }>()

const resumenEntregas = computed(() => {
  const n = props.entregas.length
  if (n === 0) return null
  const texto = n === 1 ? '1 entrega' : `${n} entregas`
  return props.plano ? `${texto} · ${props.entregas.join(', ')}` : texto
})
</script>

<template>
  <div v-if="props.compacto" class="tarjeta tarjeta--compacta">
    <span class="punto-origen" aria-hidden="true" />
    <span class="compacta__origen">{{ props.origen ?? 'Sin origen' }}</span>
    <IconArrowRight :size="18" class="compacta__flecha" aria-hidden="true" />
    <span class="compacta__entregas">{{ resumenEntregas ?? 'Sin entregas' }}</span>
    <button type="button" class="compacta__editar" aria-label="Editar puntos" @click="emit('editar')">
      <IconPencil :size="22" aria-hidden="true" />
    </button>
  </div>

  <div v-else class="tarjeta" :class="{ 'tarjeta--plana': props.plano }">
    <div class="fila">
      <span class="fila__icono" aria-hidden="true"><span class="punto-origen" /></span>
      <span class="sr-only">Origen:</span>
      <p class="campo" :class="props.origen ? 'campo--origen' : 'campo--vacio'">
        {{ props.origen ?? 'Toca el mapa para elegir' }}
      </p>
    </div>

    <div class="conector" aria-hidden="true"><span /></div>

    <div class="fila">
      <span class="fila__icono" aria-hidden="true">
        <IconMapPin v-if="resumenEntregas" :size="22" />
        <span v-else class="punto-pendiente" />
      </span>
      <span class="sr-only">Entregas:</span>
      <p class="campo" :class="{ 'campo--vacio': !resumenEntregas }">
        {{ resumenEntregas ?? (props.origen ? 'Toca el mapa para elegir' : 'Luego, tus entregas') }}
      </p>
    </div>

    <slot />
  </div>
</template>

<style scoped>
.tarjeta {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  padding: var(--space-3);
  border-radius: var(--radius-lg);
  background: var(--surface-raised);
  box-shadow: var(--shadow-control);
  pointer-events: auto;
}

.tarjeta--plana {
  padding: 0;
  background: transparent;
  box-shadow: none;
}

.fila {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.fila__icono {
  display: flex;
  flex: none;
  align-items: center;
  justify-content: center;
  width: 28px;
  color: var(--text-primary);
}

.campo {
  display: flex;
  flex: 1;
  align-items: center;
  min-width: 0;
  min-height: var(--hit-target);
  padding: 0 var(--space-3);
  border-radius: var(--radius-sm);
  background: var(--surface-sunken);
  font-size: 16px;
  line-height: 24px;
  font-weight: 500;
  color: var(--text-primary);
}

.campo--origen {
  color: var(--text-info);
}

.campo--vacio {
  font-weight: 400;
  color: var(--text-muted);
}

.conector {
  display: flex;
  justify-content: center;
  width: 28px;
  margin: -4px 0;
}

.conector span {
  height: 12px;
  border-left: 2px dotted var(--border-strong);
}

.punto-origen {
  display: block;
  flex: none;
  width: 14px;
  height: 14px;
  border-radius: var(--radius-full);
  background: var(--location);
  box-shadow:
    0 0 0 3px var(--surface-raised),
    0 0 0 6px var(--location-halo);
}

.punto-pendiente {
  display: block;
  width: 28px;
  height: 28px;
  border: 2px dashed var(--border-strong);
  border-radius: var(--radius-full);
}

/* Variante compacta (pantalla 05) */
.tarjeta--compacta {
  flex-direction: row;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-2) var(--space-2) var(--space-4);
  min-height: 56px;
  font-size: 16px;
  font-weight: 500;
}

.compacta__origen {
  color: var(--text-info);
  white-space: nowrap;
}

.compacta__flecha {
  flex: none;
  color: var(--text-secondary);
}

.compacta__entregas {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.compacta__editar {
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
  color: var(--text-primary);
}
</style>
