<script setup lang="ts">
import zumIcon from '../assets/zum-icon.svg'
import zumMark from '../assets/zum-mark.svg'

// "icono": el ícono de app (Z sobre fondo azul noche), para paneles.
// "marca": la Z sola, para pantallas grandes como la bienvenida.
// El texto toma --text-primary, así que funciona en modo claro y oscuro.
const props = withDefaults(
  defineProps<{
    variante?: 'icono' | 'marca'
    tamano?: 'sm' | 'lg' | 'xl'
    /** Etiqueta del <h1> si el logo es el título de la pantalla */
    comoTitulo?: boolean
  }>(),
  { variante: 'icono', tamano: 'sm', comoTitulo: false },
)
</script>

<template>
  <div class="logo" :class="[`logo--${props.variante}`, `logo--${props.tamano}`]">
    <img
      class="logo__img"
      :src="props.variante === 'marca' ? zumMark : zumIcon"
      alt=""
      aria-hidden="true"
    />
    <component :is="props.comoTitulo ? 'h1' : 'span'" class="logo__texto">zum</component>
  </div>
</template>

<style scoped>
.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo__texto {
  margin: 0;
  font-family: var(--font-display);
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--text-primary);
}

/* sm: cabecera del panel lateral */
.logo--sm .logo__img {
  width: 36px;
  height: 36px;
}
.logo--sm .logo__texto {
  font-size: 28px;
  line-height: 32px;
}

/* lg: bienvenida en celular */
.logo--lg {
  gap: 12px;
}
.logo--lg .logo__img {
  width: 48px;
  height: 44px;
}
.logo--lg .logo__texto {
  font-size: 44px;
  line-height: 48px;
  letter-spacing: -0.03em;
}

/* xl: bienvenida en escritorio */
.logo--xl {
  gap: 14px;
}
.logo--xl .logo__img {
  width: 60px;
  height: 55px;
}
.logo--xl .logo__texto {
  font-size: 64px;
  line-height: 64px;
  letter-spacing: -0.03em;
}
</style>
