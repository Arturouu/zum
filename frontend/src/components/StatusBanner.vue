<script setup lang="ts">
import { IconAlertCircle, IconAlertTriangle, IconCircleCheck, IconX } from '@tabler/icons-vue'
import { computed } from 'vue'

// Aviso con ícono + texto (nunca solo color). Los errores usan role="alert" para que se lean al aparecer.
const props = withDefaults(
  defineProps<{
    tono?: 'warning' | 'error' | 'success'
    /** Muestra la X para cerrarlo; emite "cerrar" */
    cerrable?: boolean
  }>(),
  { tono: 'warning', cerrable: false },
)

const emit = defineEmits<{ cerrar: [] }>()

const icono = computed(
  () => ({ warning: IconAlertTriangle, error: IconAlertCircle, success: IconCircleCheck })[props.tono],
)
</script>

<template>
  <div class="banner" :class="`banner--${props.tono}`" :role="props.tono === 'error' ? 'alert' : 'status'">
    <component :is="icono" class="banner__icono" :size="20" aria-hidden="true" />
    <p class="banner__texto"><slot /></p>
    <button v-if="props.cerrable" type="button" class="banner__cerrar" aria-label="Cerrar aviso" @click="emit('cerrar')">
      <IconX :size="18" aria-hidden="true" />
    </button>
  </div>
</template>

<style scoped>
.banner {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: var(--space-3) 14px;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-control);
  font-family: var(--font-sans);
  font-size: 14px;
  line-height: 20px;
  font-weight: 500;
  pointer-events: auto;
}

.banner__icono {
  flex: none;
}

.banner__texto {
  flex: 1;
}

.banner__cerrar {
  flex: none;
  display: flex;
  align-items: center;
  justify-content: center;
  width: var(--hit-target);
  height: var(--hit-target);
  margin: -12px -10px -12px 0;
  padding: 0;
  border: 0;
  border-radius: var(--radius-sm);
  background: transparent;
  color: inherit;
}

.banner--warning {
  background: var(--bg-warning);
  color: var(--text-warning);
}
.banner--warning .banner__icono {
  color: var(--text-warning);
}

.banner--error {
  background: var(--bg-danger);
  color: var(--text-danger);
}
.banner--error .banner__icono {
  color: var(--danger);
}

.banner--success {
  background: var(--bg-success);
  color: var(--text-success);
}
.banner--success .banner__icono {
  color: var(--success);
}
</style>
