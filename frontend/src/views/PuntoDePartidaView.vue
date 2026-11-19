<script setup lang="ts">
import { IconArrowLeft, IconCurrentLocation, IconLock, IconMap } from '@tabler/icons-vue'
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import StatusBanner from '../components/StatusBanner.vue'
import ZButton from '../components/ZButton.vue'
import { obtenerUbicacion } from '../services/ubicacion'
import { fijarOrigen, quitarOrigen, viaje } from '../stores/viaje'
import { estaDentroDeSurco } from '../utils/geo'

// Pantalla 02: el usuario elige cómo marcar su punto de partida.
const router = useRouter()
const buscando = ref(false)
const error = ref<string | null>(null)

async function usarMiUbicacion() {
  buscando.value = true
  error.value = null
  try {
    const coords = await obtenerUbicacion()
    if (estaDentroDeSurco(coords)) {
      fijarOrigen(coords, 'Tu ubicación')
    } else {
      quitarOrigen()
      viaje.aviso = {
        tono: 'warning',
        texto: 'Tu ubicación está fuera de Surco. Toca el mapa para elegir un punto dentro del distrito.',
      }
    }
    router.push('/mapa')
  } catch (e) {
    error.value = `${(e as Error).message} Puedes elegir tu punto en el mapa.`
  } finally {
    buscando.value = false
  }
}

function elegirEnMapa() {
  quitarOrigen()
  router.push('/mapa')
}
</script>

<template>
  <main class="partida">
    <header class="cabecera">
      <RouterLink to="/" class="volver" aria-label="Volver">
        <IconArrowLeft :size="22" aria-hidden="true" />
      </RouterLink>
    </header>

    <div class="cuerpo">
      <div class="ilustracion" aria-hidden="true">
        <svg width="300" height="300" viewBox="0 0 300 300">
          <rect class="manzanas" x="10" y="10" width="280" height="280" rx="40" />
          <path class="calle calle--ancha" d="M10 90H290M10 210H290M90 10V290M210 10V290" />
          <path class="calle" d="M10 150H290M150 10V290" />
          <rect class="parque" x="222" y="222" width="56" height="56" rx="8" />
          <circle class="onda onda--3" cx="150" cy="150" r="96" />
          <circle class="onda onda--2" cx="150" cy="150" r="64" />
          <circle class="onda onda--1" cx="150" cy="150" r="36" />
          <circle class="punto" cx="150" cy="150" r="16" />
        </svg>
      </div>

      <section class="contenido">
        <h1 class="text-title">¿Desde dónde sales?</h1>
        <p class="descripcion">
          Tu punto de partida es el origen de la ruta. Puedes usar tu ubicación o tocar cualquier punto
          de Surco en el mapa.
        </p>

        <StatusBanner v-if="error" tono="error" cerrable class="aviso" @cerrar="error = null">
          {{ error }}
        </StatusBanner>

        <div class="acciones">
          <ZButton tamano="lg" bloque :cargando="buscando" @click="usarMiUbicacion">
            <template #icono><IconCurrentLocation :size="20" aria-hidden="true" /></template>
            {{ buscando ? 'Buscando tu ubicación…' : 'Usar mi ubicación' }}
          </ZButton>
          <ZButton variante="secondary" tamano="lg" bloque @click="elegirEnMapa">
            <template #icono><IconMap :size="20" aria-hidden="true" /></template>
            Elegir en el mapa
          </ZButton>
          <p class="privacidad">
            <IconLock :size="16" aria-hidden="true" />
            Tu ubicación solo se usa para calcular la ruta. No la guardamos.
          </p>
        </div>
      </section>
    </div>
  </main>
</template>

<style scoped>
.partida {
  display: flex;
  flex-direction: column;
  min-height: 100dvh;
  background: var(--bg-page);
}

.cabecera {
  display: flex;
  align-items: center;
  height: 64px;
  padding: var(--space-2) var(--space-2) 0;
}

.volver {
  display: flex;
  align-items: center;
  justify-content: center;
  width: var(--hit-target);
  height: var(--hit-target);
  border-radius: var(--radius-md);
  color: var(--text-primary);
}

.cuerpo {
  display: flex;
  flex: 1;
  flex-direction: column;
}

.ilustracion {
  display: flex;
  flex: none;
  align-items: center;
  justify-content: center;
  height: 330px;
}

.ilustracion svg {
  max-width: 100%;
  height: auto;
}

.manzanas {
  fill: var(--map-ground);
}
.calle {
  fill: none;
  stroke: var(--map-street);
  stroke-width: 5;
}
.calle--ancha {
  stroke-width: 12;
}
.parque {
  fill: var(--map-park);
}
.onda {
  fill: var(--location);
}
.onda--1 {
  fill-opacity: 0.22;
}
.onda--2 {
  fill-opacity: 0.12;
}
.onda--3 {
  fill: none;
  stroke: var(--location);
  stroke-opacity: 0.18;
  stroke-width: 2;
}
.punto {
  fill: var(--location);
  stroke: var(--map-street);
  stroke-width: 5;
}

.contenido {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: var(--space-3);
  padding: 0 var(--space-5) var(--space-6);
}

.descripcion {
  color: var(--text-secondary);
}

.aviso {
  box-shadow: none;
}

.acciones {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  margin-top: auto;
  padding-top: var(--space-5);
}

.privacidad {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  margin-top: var(--space-1);
  font-size: 13px;
  line-height: 18px;
  font-weight: 500;
  color: var(--text-secondary);
}

.privacidad svg {
  flex: none;
  margin-top: 1px;
}

/* En escritorio la pantalla se centra en una columna */
@media (min-width: 768px) {
  .cuerpo {
    justify-content: center;
    width: 100%;
    max-width: 480px;
    margin: 0 auto;
    padding-bottom: 64px;
  }

  .contenido {
    flex: none;
  }

  .acciones {
    margin-top: var(--space-3);
  }
}
</style>
