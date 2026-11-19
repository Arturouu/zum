<script setup lang="ts">
import { IconArrowRight, IconMapPin, IconRoute, IconTarget } from '@tabler/icons-vue'
import AppLogo from '../components/AppLogo.vue'
import IlustracionMapa from '../components/IlustracionMapa.vue'
import ZButton from '../components/ZButton.vue'
import { useEsEscritorio } from '../composables/useMediaQuery'

// Pantallas 01 (celular) y 09 (escritorio). Sigue el tema del sistema, como el resto de la app.
const esEscritorio = useEsEscritorio()
</script>

<template>
  <main class="bienvenida">
    <div class="ilustracion">
      <IlustracionMapa :radio-parada="esEscritorio ? 12 : 28" />
    </div>

    <section class="contenido">
      <AppLogo variante="marca" :tamano="esEscritorio ? 'xl' : 'lg'" como-titulo />
      <p class="lema">De la A a la Z, sin vueltas.</p>

      <p v-if="esEscritorio" class="descripcion">
        Marca tu punto de partida y hasta 10 entregas en Santiago de Surco. Zum calcula el orden de
        visita con la menor distancia total y te dibuja la ruta calle por calle.
      </p>
      <ol v-else class="pasos">
        <li>
          <span class="pasos__icono pasos__icono--info"><IconTarget :size="18" aria-hidden="true" /></span>
          Marca desde dónde sales
        </li>
        <li>
          <span class="pasos__icono"><IconMapPin :size="18" aria-hidden="true" /></span>
          Toca el mapa para sumar hasta 10 entregas
        </li>
        <li>
          <span class="pasos__icono pasos__icono--marca"><IconRoute :size="18" aria-hidden="true" /></span>
          Te damos el orden más corto
        </li>
      </ol>

      <div class="acciones">
        <ZButton to="/inicio" tamano="lg" :bloque="!esEscritorio">
          Comenzar
          <template #icono-final><IconArrowRight :size="20" stroke="2.2" aria-hidden="true" /></template>
        </ZButton>
        <p class="nota">Sin registro · Solo en Santiago de Surco</p>
      </div>
    </section>
  </main>
</template>

<style scoped>
.bienvenida {
  display: flex;
  flex-direction: column;
  min-height: 100dvh;
  background: var(--bg-page);
  color: var(--text-primary);
}

/* ---------- Ilustración ---------- */
.ilustracion {
  position: relative;
  flex: none;
  height: min(440px, 52dvh);
  overflow: hidden;
}

/* En celular el mapa se funde con el fondo antes del texto */
.ilustracion::after {
  content: '';
  position: absolute;
  inset: auto 0 0;
  height: 72px;
  background: linear-gradient(transparent, var(--bg-page));
}

/* ---------- Texto ---------- */
.contenido {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 20px;
  padding: var(--space-2) var(--space-5) var(--space-6);
}

.lema {
  margin-top: -8px;
  font-family: var(--font-display);
  font-size: 22px;
  line-height: 28px;
  font-weight: 600;
}

.pasos {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  padding: 0;
  list-style: none;
}

.pasos li {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  color: var(--text-secondary);
  line-height: 22px;
}

.pasos__icono {
  display: flex;
  flex: none;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: 1px solid var(--border);
  border-radius: var(--radius-full);
  background: var(--surface);
  color: var(--text-primary);
}
.pasos__icono--info {
  color: var(--text-info);
}
.pasos__icono--marca {
  color: var(--text-brand);
}

.acciones {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  margin-top: auto;
}

.nota {
  font-size: 13px;
  line-height: 18px;
  font-weight: 500;
  color: var(--text-secondary);
  text-align: center;
}

/* ---------- Escritorio (pantalla 09) ---------- */
@media (min-width: 768px) {
  .bienvenida {
    flex-direction: row-reverse;
    height: 100dvh;
  }

  .ilustracion {
    flex: 999 1 520px;
    height: auto;
    border-left: 1px solid var(--border);
  }

  .ilustracion::after {
    display: none;
  }

  .contenido {
    flex: 1 1 420px;
    justify-content: center;
    gap: 28px;
    padding: 64px clamp(24px, 6vw, 96px);
  }

  .lema {
    max-width: 30rem;
    margin-top: 0;
    font-size: 32px;
    line-height: 40px;
  }

  .descripcion {
    max-width: 30rem;
    font-size: 18px;
    line-height: 28px;
    color: var(--text-secondary);
  }

  .acciones {
    flex-direction: row;
    flex-wrap: wrap;
    align-items: center;
    gap: var(--space-4);
    margin-top: 0;
  }

  .nota {
    font-size: 14px;
    line-height: 20px;
    text-align: left;
  }
}
</style>
