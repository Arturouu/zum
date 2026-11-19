<script setup lang="ts">
import { IconArrowRight, IconTarget, IconMapPin, IconRoute } from '@tabler/icons-vue'
import AppLogo from '../components/AppLogo.vue'
import ZButton from '../components/ZButton.vue'
import { computed } from 'vue'
import { useEsEscritorio } from '../composables/useMediaQuery'

// Pantallas 01 (celular) y 09 (escritorio). Siempre en modo oscuro: fondo azul noche.
const esEscritorio = useEsEscritorio()

// Medidas de la ilustración (la Z de ruta) copiadas de los mockups 01 y 09
const ILUSTRACION_MOVIL = {
  viewBox: '0 0 390 440',
  callesAnchas: 'M0 50H390M0 150H390M0 250H390M0 350H390M30 0V440M130 0V440M230 0V440M330 0V440',
  callesAngostas: 'M0 100H390M0 200H390M0 300H390M0 400H390M80 0V440M180 0V440M280 0V440M380 0V440',
  anchoCalle: 12,
  parques: [{ x: 186, y: 206, width: 88, height: 88, rx: 10 }],
  ruta: 'M64 112 H318 L84 332 H330',
  anchoRuta: 22,
  guion: '10 10',
  origen: [64, 112],
  paradas: [
    [318, 112],
    [84, 332],
    [330, 332],
  ],
  radioParada: 18,
}

const ILUSTRACION_ESCRITORIO = {
  viewBox: '0 0 760 900',
  callesAnchas:
    'M0 100H760M0 250H760M0 400H760M0 550H760M0 700H760M0 850H760M60 0V900M210 0V900M360 0V900M510 0V900M660 0V900',
  callesAngostas:
    'M0 175H760M0 325H760M0 475H760M0 625H760M0 775H760M135 0V900M285 0V900M435 0V900M585 0V900M735 0V900',
  anchoCalle: 16,
  parques: [
    { x: 378, y: 418, width: 114, height: 114, rx: 12 },
    { x: 78, y: 718, width: 114, height: 114, rx: 12 },
  ],
  ruta: 'M150 250 H600 L170 650 H620',
  anchoRuta: 30,
  guion: '14 14',
  origen: [150, 250],
  paradas: [
    [600, 250],
    [170, 650],
    [620, 650],
  ],
  radioParada: 24,
}

const z = computed(() => (esEscritorio.value ? ILUSTRACION_ESCRITORIO : ILUSTRACION_MOVIL))
</script>

<template>
  <main class="bienvenida" data-theme="dark">
    <div class="ilustracion" aria-hidden="true">
      <svg :viewBox="z.viewBox" preserveAspectRatio="xMidYMid slice">
        <path class="calle-ancha" :d="z.callesAnchas" :stroke-width="z.anchoCalle" />
        <path class="calle-angosta" :d="z.callesAngostas" :stroke-width="z.anchoCalle / 3" />
        <rect v-for="(p, i) in z.parques" :key="i" class="parque" v-bind="p" />
        <g class="ruta">
          <path class="ruta__borde" :d="z.ruta" :stroke-width="z.anchoRuta * 1.35" />
          <path class="ruta__linea" :d="z.ruta" :stroke-width="z.anchoRuta" />
          <path class="ruta__guion" :d="z.ruta" :stroke-width="z.anchoRuta / 9" :stroke-dasharray="z.guion" />
        </g>
        <circle class="origen__halo" :cx="z.origen[0]" :cy="z.origen[1]" :r="z.radioParada * 1.7" />
        <circle
          class="origen"
          :cx="z.origen[0]"
          :cy="z.origen[1]"
          :r="z.radioParada * 0.73"
          :stroke-width="z.radioParada / 5"
        />
        <g class="parada" :font-size="z.radioParada * 0.93">
          <template v-for="(c, i) in z.paradas" :key="i">
            <circle :cx="c[0]" :cy="c[1]" :r="z.radioParada" :stroke-width="z.radioParada / 5" />
            <text :x="c[0]" :y="c[1] + z.radioParada / 3">{{ i + 1 }}</text>
          </template>
        </g>
      </svg>
    </div>

    <section class="contenido">
      <AppLogo variante="oscura" :tamano="esEscritorio ? 'xl' : 'lg'" como-titulo />
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
  background: var(--night-900);
  color: var(--text-primary);
}

/* ---------- Ilustración: la Z de ruta sobre un mapa ---------- */
.ilustracion {
  position: relative;
  flex: none;
  height: min(440px, 52dvh);
  overflow: hidden;
  background: var(--night-900);
}

/* En celular la cuadrícula se funde con el fondo antes del texto */
.ilustracion::after {
  content: '';
  position: absolute;
  inset: auto 0 0;
  height: 64px;
  background: linear-gradient(transparent, var(--night-900));
}

.ilustracion svg {
  display: block;
  width: 100%;
  height: 100%;
}

.calle-ancha,
.calle-angosta {
  fill: none;
}
.calle-ancha {
  stroke: var(--map-street);
}
.calle-angosta {
  stroke: var(--surface);
}
.parque {
  fill: var(--map-park);
}

.ruta path {
  fill: none;
  stroke-linecap: round;
  stroke-linejoin: round;
}
.ruta__borde {
  stroke: var(--route-casing);
}
.ruta__linea {
  stroke: var(--brand);
}
.ruta__guion {
  stroke: var(--text-primary);
}

.origen__halo {
  fill: var(--location);
  fill-opacity: 0.25;
}
.origen {
  fill: var(--location);
  stroke: var(--night-900);
}

.parada circle {
  fill: var(--surface-inverse);
  stroke: var(--night-900);
}
.parada text {
  fill: var(--text-on-inverse);
  font-family: var(--font-sans);
  font-weight: 600;
  text-anchor: middle;
}

/* ---------- Texto ---------- */
.contenido {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 20px;
  padding: var(--space-4) var(--space-5) var(--space-6);
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
  border-radius: var(--radius-full);
  background: var(--surface-raised);
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
    background: var(--map-ground);
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
