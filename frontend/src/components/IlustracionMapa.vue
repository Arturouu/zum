<script setup lang="ts">
// Mapa ilustrado de la bienvenida: manzanas, calles, una avenida, parques, una laguna
// y una ruta corta por las calles (origen + 3 paradas). Los colores salen de tokens.css,
// así que también se adapta al modo oscuro. Los trazos usan non-scaling-stroke para
// medir lo mismo en px en celular y en escritorio.
const props = withDefaults(defineProps<{ radioParada?: number }>(), { radioParada: 14 })

// Cada parque ocupa una manzana (o parte de ella) que no cruza la avenida
const PARQUES = [
  { x: 228, y: 238, w: 144, h: 134 },
  { x: 548, y: 538, w: 144, h: 134 },
  { x: 228, y: 688, w: 144, h: 134 },
  { x: 388, y: 88, w: 144, h: 134 },
  { x: 388, y: 538, w: 144, h: 134 },
  { x: 708, y: 688, w: 144, h: 134 },
  { x: 708, y: 388, w: 66, h: 134 },
  { x: 68, y: 163, w: 64, h: 59 },
  { x: 68, y: 238, w: 64, h: 60 },
  { x: 468, y: 763, w: 64, h: 59 },
]

// Árboles: unos puntos dentro de cada parque
const ARBOLES = PARQUES.flatMap((p) => {
  const puntos: [number, number][] = []
  for (let fx = 0.25; fx < 1; fx += 0.25) {
    for (let fy = 0.3; fy < 1; fy += 0.4) {
      if (p.w > 100 || fx === 0.5) puntos.push([p.x + p.w * fx, p.y + p.h * fy + (fx === 0.5 ? 10 : 0)])
    }
  }
  return puntos
})

const CALLES_PRINCIPALES =
  'M0 80H800M0 230H800M0 380H800M0 530H800M0 680H800M0 830H800M60 0V900M220 0V900M380 0V900M540 0V900M700 0V900'
const CALLES_SECUNDARIAS =
  'M0 155H800M0 305H800M0 455H800M0 605H800M0 755H800M140 0V900M300 0V900M460 0V900M620 0V900M780 0V900'
const AVENIDA = 'M-40 860 L840 100'
const RUTA = 'M220 680 V530 H540 V380 H380 V230'
const ORIGEN: [number, number] = [220, 680]
const PARADAS: [number, number][] = [
  [540, 530],
  [380, 380],
  [380, 230],
]
</script>

<template>
  <svg class="ilustracion-mapa" viewBox="0 0 800 900" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
    <rect class="suelo" x="-100" y="-100" width="1000" height="1100" />
    <path class="calle calle--secundaria" :d="CALLES_SECUNDARIAS" />

    <rect v-for="(p, i) in PARQUES" :key="`p${i}`" class="parque" :x="p.x" :y="p.y" :width="p.w" :height="p.h" rx="12" />
    <circle v-for="(a, i) in ARBOLES" :key="`a${i}`" class="arbol" :cx="a[0]" :cy="a[1]" r="9" />
    <ellipse class="laguna" cx="140" cy="455" rx="66" ry="48" />

    <path class="calle calle--principal" :d="CALLES_PRINCIPALES" />
    <path class="avenida avenida--borde" :d="AVENIDA" />
    <path class="avenida" :d="AVENIDA" />

    <path class="ruta ruta--borde" :d="RUTA" />
    <path class="ruta" :d="RUTA" />

    <circle class="origen-halo" :cx="ORIGEN[0]" :cy="ORIGEN[1]" :r="props.radioParada * 1.5" />
    <circle class="origen" :cx="ORIGEN[0]" :cy="ORIGEN[1]" :r="props.radioParada * 0.6" />
    <g v-for="(c, i) in PARADAS" :key="`s${i}`" class="parada">
      <circle :cx="c[0]" :cy="c[1]" :r="props.radioParada" />
      <text :x="c[0]" :y="c[1]" :font-size="props.radioParada" dy="0.36em">{{ i + 1 }}</text>
    </g>
  </svg>
</template>

<style scoped>
.ilustracion-mapa {
  display: block;
  width: 100%;
  height: 100%;
}

.ilustracion-mapa :is(path, circle, ellipse) {
  vector-effect: non-scaling-stroke;
}

.suelo {
  fill: var(--map-ground);
}

.calle {
  fill: none;
  stroke: var(--map-street);
}
.calle--principal {
  stroke-width: 12;
}
.calle--secundaria {
  stroke-width: 5;
}

.parque {
  fill: var(--map-park);
}
.arbol {
  fill: var(--success);
  fill-opacity: 0.18;
}
.laguna {
  fill: var(--location-halo);
}

.avenida {
  fill: none;
  stroke: var(--bg-warning);
  stroke-width: 20;
  stroke-linecap: round;
}
.avenida--borde {
  stroke: var(--border);
  stroke-width: 24;
}

.ruta {
  fill: none;
  stroke: var(--brand);
  stroke-width: 6;
  stroke-linecap: round;
  stroke-linejoin: round;
}
.ruta--borde {
  stroke: var(--route-casing);
  stroke-width: 10;
}

.origen-halo {
  fill: var(--location-halo);
}
.origen {
  fill: var(--location);
  stroke: #ffffff;
  stroke-width: 3;
}

.parada circle {
  fill: var(--surface-inverse);
  stroke: var(--surface);
  stroke-width: 2;
}
.parada text {
  fill: var(--text-on-inverse);
  font-family: var(--font-sans);
  font-weight: 600;
  text-anchor: middle;
}
</style>
