/**
 * Genera un identificador de ancla estable a partir del titulo de una seccion.
 *
 * Se usa tanto al renderizar `<section id="...">` como al construir los enlaces
 * del indice, del buscador y del asistente. Debe ser la unica implementacion:
 * si el algoritmo cambia en un sitio y no en otro, los anclajes dejan de
 * resolver silenciosamente.
 */
export function slugify(text: string): string {
  return text
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "") // quita diacriticos: "Admision" -> "admision"
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
}
