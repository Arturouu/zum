<script setup lang="ts">
import { IconCurrentLocation, IconMinus, IconPlus, IconRoute } from '@tabler/icons-vue'
import { Map as MapaLibre, setWorkerUrl, type MapMouseEvent, type Marker } from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'
import urlWorkerMapLibre from 'maplibre-gl/dist/maplibre-gl-worker.mjs?url'
import { computed, onBeforeUnmount, onMounted, ref, shallowRef, watch } from 'vue'
import zumIcon from '../assets/zum-icon.svg'
import AppLogo from '../components/AppLogo.vue'
import BottomSheet from '../components/BottomSheet.vue'
import LocationCard from '../components/LocationCard.vue'
import MapControl from '../components/MapControl.vue'
import StatusBanner from '../components/StatusBanner.vue'
import StopList from '../components/StopList.vue'
import ZButton from '../components/ZButton.vue'
import { useEsEscritorio, useMediaQuery } from '../composables/useMediaQuery'
import { agregarCapasRuta, agregarLimiteSurco } from '../map/capas'
import {
  CENTRO_SURCO,
  ESTILO_CLARO,
  ESTILO_OSCURO,
  LIMITES_MAPA,
  ZOOM_INICIAL,
  ZOOM_MINIMO,
  ZOOM_PUNTO,
} from '../map/config'
import { crearMarcadorOrigen, crearMarcadorParada } from '../map/marcadores'
import { calcularRuta } from '../services/route'
import { obtenerUbicacion } from '../services/ubicacion'
import { agregarEntrega, fijarOrigen, MAX_ENTREGAS, quitarEntrega, viaje, type Aviso } from '../stores/viaje'
import type { LngLat } from '../types/ruta'
import { estaDentroDeSurco } from '../utils/geo'
import { letraEntrega } from '../utils/formato'

// Pantallas 03 a 06 en una sola vista. El mapa se crea una vez y no se destruye al cambiar de estado.
// Por ahora implementa el estado "sin-entregas" (03): elegir el origen y ver Surco.
// Los estados con-entregas → calculando → ruta-lista → pasos quedan para el equipo (ver los TODO(equipo)).

const esEscritorio = useEsEscritorio()
const modoOscuro = useMediaQuery('(prefers-color-scheme: dark)')

const contenedor = ref<HTMLDivElement>()
const mapa = shallowRef<MapaLibre>()
let marcadorOrigen: Marker | null = null
let marcadoresEntregas: Marker[] = []

const aviso = ref<Aviso | null>(viaje.aviso)
viaje.aviso = null
const buscandoUbicacion = ref(false)

const AVISO_FUERA: Aviso = { tono: 'warning', texto: 'Ese punto está fuera de Surco. Elige uno dentro del distrito.' }

// ---------- Mapa ----------

// MapLibre busca su worker junto a su propio archivo, pero Vite lo pre-empaqueta en otra
// carpeta y no lo encuentra ("Worker failed to load"). Se le indica la URL a mano.
setWorkerUrl(urlWorkerMapLibre)

onMounted(() => {
  const m = new MapaLibre({
    container: contenedor.value!,
    style: modoOscuro.value ? ESTILO_OSCURO : ESTILO_CLARO,
    center: viaje.origen ?? CENTRO_SURCO,
    zoom: viaje.origen ? ZOOM_PUNTO : ZOOM_INICIAL,
    minZoom: ZOOM_MINIMO,
    maxBounds: LIMITES_MAPA,
    attributionControl: false, // la atribución se muestra en la hoja / esquina (ver template)
    dragRotate: false,
    pitchWithRotate: false,
  })
  m.touchZoomRotate.disableRotation()

  // "style.load" se dispara al cargar y cada vez que cambia el estilo (claro ↔ oscuro)
  m.on('style.load', () => {
    agregarLimiteSurco(m, modoOscuro.value)
    agregarCapasRuta(m)
  })
  m.on('click', alTocarMapa)

  mapa.value = m
  dibujarOrigen()
  dibujarEntregas()
})

onBeforeUnmount(() => {
  marcadorOrigen?.remove()
  marcadoresEntregas.forEach((m) => m.remove())
  mapa.value?.remove()
})

watch(modoOscuro, (oscuro) => mapa.value?.setStyle(oscuro ? ESTILO_OSCURO : ESTILO_CLARO, { diff: false }))

// ---------- Origen ----------

function dibujarOrigen() {
  const m = mapa.value
  if (!m) return
  if (!viaje.origen) {
    marcadorOrigen?.remove()
    marcadorOrigen = null
    return
  }
  if (!marcadorOrigen) {
    marcadorOrigen = crearMarcadorOrigen(viaje.origen).addTo(m)
    marcadorOrigen.on('dragend', alSoltarOrigen)
  } else {
    marcadorOrigen.setLngLat(viaje.origen)
  }
}

watch(() => viaje.origen, dibujarOrigen)

function alSoltarOrigen() {
  const { lng, lat } = marcadorOrigen!.getLngLat()
  const punto: LngLat = [lng, lat]
  if (estaDentroDeSurco(punto)) {
    fijarOrigen(punto, 'Punto en el mapa')
    aviso.value = null
  } else {
    marcadorOrigen!.setLngLat(viaje.origen!) // vuelve a donde estaba
    aviso.value = AVISO_FUERA
  }
}

function alTocarMapa(e: MapMouseEvent) {
  const punto: LngLat = [e.lngLat.lng, e.lngLat.lat]
  if (!estaDentroDeSurco(punto)) {
    aviso.value = AVISO_FUERA
    return
  }
  aviso.value = null

  if (!viaje.origen) {
    fijarOrigen(punto, 'Punto en el mapa')
    return
  }

  agregar(punto)
}

// ---------- Entregas (pantalla 04) ----------

const hayEntregas = computed(() => viaje.entregas.length > 0)
const enLimite = computed(() => viaje.entregas.length >= MAX_ENTREGAS)
const tituloEntregas = computed(() => {
  const n = viaje.entregas.length
  return `${n} ${n === 1 ? 'entrega' : 'entregas'}`
})
const paradas = computed(() =>
  viaje.entregas.map((e, i) => ({
    id: e.id,
    marcador: letraEntrega(i),
    titulo: `Entrega ${letraEntrega(i)}`,
  })),
)

function avisarLimite() {
  aviso.value = { tono: 'warning', texto: `Llegaste al máximo de ${MAX_ENTREGAS} entregas. Quita una para agregar otra.` }
}

function agregar(punto: LngLat) {
  if (!agregarEntrega(punto)) avisarLimite()
}

// El botón "Agregar entrega" solo orienta: las entregas se marcan tocando el mapa.
function pedirEntrega() {
  if (enLimite.value) return avisarLimite()
  aviso.value = { tono: 'success', texto: 'Toca el mapa para marcar la siguiente entrega.' }
}

function dibujarEntregas() {
  const m = mapa.value
  if (!m) return
  // Máximo 10 marcadores: más simple recrearlos que renombrar letras al quitar una entrega
  marcadoresEntregas.forEach((marcador) => marcador.remove())
  marcadoresEntregas = viaje.entregas.map((e, i) => crearMarcadorParada(letraEntrega(i), e.coords).addTo(m))
}

watch(() => viaje.entregas, dibujarEntregas, { deep: true })

async function centrarEnMiUbicacion() {
  buscandoUbicacion.value = true
  try {
    const coords = await obtenerUbicacion()
    if (!estaDentroDeSurco(coords)) {
      aviso.value = { tono: 'warning', texto: 'Tu ubicación está fuera de Surco. Toca el mapa para elegir un punto.' }
      return
    }
    if (!viaje.origen) fijarOrigen(coords, 'Tu ubicación')
    mapa.value?.flyTo({ center: coords, zoom: ZOOM_PUNTO })
  } catch (e) {
    aviso.value = { tono: 'error', texto: (e as Error).message }
  } finally {
    buscandoUbicacion.value = false
  }
}

// ---------- Calcular ----------

const calculando = ref(false)

async function calcular() {
  if (calculando.value) return
  if (viaje.entregas.length === 0 || !viaje.origen) {
    aviso.value = { tono: 'warning', texto: 'Agrega al menos una entrega para calcular la ruta.' }
    return
  }
  aviso.value = null
  calculando.value = true
  try {
    viaje.ruta = await calcularRuta({
      origin: viaje.origen,
      deliveries: viaje.entregas.map((e) => e.coords),
    })
  } catch (e) {
    aviso.value = { tono: 'error', texto: (e as Error).message }
  } finally {
    calculando.value = false
  }
}
</script>

<template>
  <main class="vista">
    <div ref="contenedor" class="mapa" role="region" aria-label="Mapa de Santiago de Surco" />

    <!-- Celular: tarjeta flotante arriba -->
    <div v-if="!esEscritorio" class="capa-superior">
      <LocationCard :origen="viaje.nombreOrigen" :entregas="viaje.entregas.map((_, i) => letraEntrega(i))" />
    </div>

    <!-- Escritorio: controles arriba a la derecha y atribución en la esquina del mapa -->
    <template v-if="esEscritorio">
      <div class="controles-escritorio">
        <MapControl etiqueta="Acercar" @click="mapa?.zoomIn()"><IconPlus :size="22" aria-hidden="true" /></MapControl>
        <MapControl etiqueta="Alejar" @click="mapa?.zoomOut()"><IconMinus :size="22" aria-hidden="true" /></MapControl>
        <MapControl etiqueta="Usar mi ubicación" tono="info" :aria-busy="buscandoUbicacion" @click="centrarEnMiUbicacion">
          <IconCurrentLocation :size="22" aria-hidden="true" />
        </MapControl>
      </div>
      <StatusBanner v-if="aviso" :tono="aviso.tono" cerrable class="aviso-escritorio" @cerrar="aviso = null">
        {{ aviso.texto }}
      </StatusBanner>
      <p class="atribucion atribucion--mapa">
        © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> ·
        <a href="https://openfreemap.org" target="_blank" rel="noopener">OpenFreeMap</a>
      </p>
    </template>

    <div class="capa-inferior">
      <template v-if="!esEscritorio">
        <MapControl
          etiqueta="Usar mi ubicación"
          tono="info"
          class="control-ubicacion"
          :aria-busy="buscandoUbicacion"
          @click="centrarEnMiUbicacion"
        >
          <IconCurrentLocation :size="22" aria-hidden="true" />
        </MapControl>
        <StatusBanner v-if="aviso" :tono="aviso.tono" cerrable class="aviso-movil" @cerrar="aviso = null">
          {{ aviso.texto }}
        </StatusBanner>
      </template>

      <BottomSheet etiqueta="Tu ruta" class="hoja">
        <AppLogo v-if="esEscritorio" />
        <LocationCard
          v-if="esEscritorio"
          plano
          :origen="viaje.nombreOrigen"
          :entregas="viaje.entregas.map((_, i) => letraEntrega(i))"
        />

        <div class="titulo">
          <img v-if="!esEscritorio" :src="zumIcon" alt="" width="32" height="32" />
          <h1 class="text-heading">Tu ruta de hoy</h1>
        </div>
        <p v-if="!hayEntregas" class="indicacion">
          <template v-if="!viaje.origen">Toca el mapa para elegir tu punto de partida dentro de Surco.</template>
          <template v-else>
            Toca el mapa para agregar tu primera entrega. Puedes sumar hasta {{ MAX_ENTREGAS }}.
          </template>
        </p>

        <template v-else>
          <div class="encabezado-entregas">
            <h2 class="text-heading">{{ tituloEntregas }}</h2>
            <span class="limite">Máximo {{ MAX_ENTREGAS }}</span>
          </div>
          <StopList :paradas="paradas" quitable @quitar="quitarEntrega" />
          <button type="button" class="agregar" @click="pedirEntrega">
            <IconPlus :size="18" aria-hidden="true" />
            Agregar entrega
          </button>
        </template>

        <ZButton bloque :cargando="calculando" @click="calcular">
          <template #icono><IconRoute :size="20" aria-hidden="true" /></template>
          {{ calculando ? 'Calculando…' : 'Calcular ruta' }}
        </ZButton>

        <p v-if="!esEscritorio" class="atribucion">
          © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> ·
          <a href="https://openfreemap.org" target="_blank" rel="noopener">OpenFreeMap</a>
        </p>
      </BottomSheet>
    </div>
  </main>
</template>

<style scoped>
/* ---------- Celular: mapa a pantalla completa con capas encima ---------- */
.vista {
  position: relative;
  height: 100dvh;
  overflow: hidden;
  background: var(--map-ground);
}

.mapa {
  position: absolute;
  inset: 0;
}

.capa-superior {
  position: absolute;
  top: var(--space-4);
  right: var(--space-4);
  left: var(--space-4);
  pointer-events: none;
}

.capa-inferior {
  position: absolute;
  right: 0;
  bottom: 0;
  left: 0;
  display: flex;
  flex-direction: column;
  pointer-events: none; /* deja tocar el mapa en los huecos */
}

.control-ubicacion {
  align-self: flex-end;
  margin: 0 var(--space-4) var(--space-4);
}

.aviso-movil {
  margin: 0 var(--space-4) var(--space-3);
}

.titulo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.indicacion {
  color: var(--text-secondary);
}

.encabezado-entregas {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
}

.limite {
  font-size: 14px;
  line-height: 20px;
  font-weight: 500;
  color: var(--text-secondary);
}

.agregar {
  display: flex;
  align-items: center;
  gap: 6px;
  align-self: flex-start;
  height: var(--hit-target);
  padding: 0 var(--space-1);
  border: 0;
  background: transparent;
  color: var(--text-danger);
  font: inherit;
  font-weight: 600;
  cursor: pointer;
}

.atribucion {
  font-size: 12px;
  line-height: 16px;
  font-weight: 500;
  color: var(--text-secondary);
  text-align: center;
}

.atribucion a {
  color: inherit;
  text-decoration: none;
}

.atribucion a:hover {
  text-decoration: underline;
}

/* ---------- Escritorio: panel lateral + mapa ---------- */
@media (min-width: 768px) {
  .vista {
    display: grid;
    grid-template-columns: var(--sidebar-width) 1fr;
  }

  .mapa {
    position: relative;
    grid-row: 1;
    grid-column: 2;
    inset: auto;
  }

  .capa-inferior {
    position: static;
    grid-row: 1;
    grid-column: 1;
    pointer-events: auto;
  }

  .hoja {
    flex: 1;
  }

  .controles-escritorio {
    position: absolute;
    top: var(--space-5);
    right: var(--space-5);
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
  }

  .aviso-escritorio {
    position: absolute;
    top: var(--space-5);
    left: calc(var(--sidebar-width) + var(--space-5));
    max-width: 440px;
  }

  .atribucion--mapa {
    position: absolute;
    right: var(--space-3);
    bottom: var(--space-2);
    padding: 2px var(--space-2);
    border-radius: 6px;
    background: color-mix(in srgb, var(--surface) 85%, transparent);
  }
}
</style>
