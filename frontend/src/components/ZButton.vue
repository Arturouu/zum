<script setup lang="ts">
import { RouterLink, type RouteLocationRaw } from 'vue-router'

// Botón del design system. Con `to` se comporta como enlace de vue-router.
// El ícono va en el slot "icono" (antes del texto) o "icono-final" (después).
const props = withDefaults(
  defineProps<{
    variante?: 'primary' | 'secondary' | 'ghost' | 'danger'
    tamano?: 'md' | 'lg'
    bloque?: boolean
    to?: RouteLocationRaw
    type?: 'button' | 'submit'
    disabled?: boolean
    cargando?: boolean
  }>(),
  { variante: 'primary', tamano: 'md', bloque: false, type: 'button', disabled: false, cargando: false },
)
</script>

<template>
  <RouterLink
    v-if="props.to"
    :to="props.to"
    class="zbtn"
    :class="[`zbtn--${props.variante}`, `zbtn--${props.tamano}`, { 'zbtn--bloque': props.bloque }]"
  >
    <slot name="icono" />
    <slot />
    <slot name="icono-final" />
  </RouterLink>
  <button
    v-else
    :type="props.type"
    class="zbtn"
    :class="[`zbtn--${props.variante}`, `zbtn--${props.tamano}`, { 'zbtn--bloque': props.bloque }]"
    :disabled="props.disabled || props.cargando"
    :aria-busy="props.cargando || undefined"
  >
    <slot name="icono" />
    <slot />
    <slot name="icono-final" />
  </button>
</template>

<style scoped>
.zbtn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  height: var(--button-height);
  padding: 0 var(--space-5);
  border: 1px solid transparent;
  border-radius: var(--radius-md);
  font-family: var(--font-sans);
  font-size: 16px;
  line-height: 24px;
  font-weight: 600;
  text-decoration: none;
  white-space: nowrap;
  transition: background-color 0.15s ease;
}

.zbtn--lg {
  height: 56px;
  font-size: 18px;
}

.zbtn--bloque {
  display: flex;
  width: 100%;
}

.zbtn :deep(svg) {
  flex: none;
}

/* Regla del handoff: el texto sobre coral es azul noche, nunca blanco */
.zbtn--primary {
  background: var(--brand);
  color: var(--text-on-brand);
}
.zbtn--primary:hover:not(:disabled) {
  background: var(--brand-hover);
}

.zbtn--secondary {
  background: var(--surface);
  border-color: var(--border-strong);
  color: var(--text-primary);
}
.zbtn--secondary:hover:not(:disabled) {
  background: var(--surface-sunken);
}

.zbtn--ghost {
  height: var(--hit-target);
  padding: 0 var(--space-1);
  background: transparent;
  color: var(--text-brand);
}

.zbtn--danger {
  background: transparent;
  border-color: var(--text-danger);
  color: var(--text-danger);
}
.zbtn--danger:hover:not(:disabled) {
  background: var(--bg-danger);
}

.zbtn:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}

.zbtn[aria-busy='true'] {
  cursor: progress;
  opacity: 1;
}
</style>
