import { onBeforeUnmount, ref } from 'vue'

/** Devuelve un ref que sigue a la media query, p. ej. useMediaQuery('(min-width: 768px)') */
export function useMediaQuery(query: string) {
  const mql = window.matchMedia(query)
  const coincide = ref(mql.matches)
  const actualizar = (e: MediaQueryListEvent) => (coincide.value = e.matches)

  mql.addEventListener('change', actualizar)
  onBeforeUnmount(() => mql.removeEventListener('change', actualizar))

  return coincide
}

/** Desde 768 px la hoja inferior pasa a ser panel lateral */
export const useEsEscritorio = () => useMediaQuery('(min-width: 768px)')
