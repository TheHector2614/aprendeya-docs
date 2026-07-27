# Gestión Documental — AprendeYa

Estructura de organización, categorización y administración de los documentos corporativos de la plataforma educativa AprendeYa.

## Etapas del pipeline

```
Etapa 1 ← TÚ ESTÁS AQUÍ
  Recolección y Organización
       ↓
Etapa 2
  Procesamiento e Indexación
       ↓
Etapa 3
  Búsqueda y Generación de Respuestas
```

## Archivos del directorio

| Archivo | Propósito |
|---|---|
| `inventario.yaml` | Registro maestro de todos los documentos: metadatos, fuente, formato, responsable |
| `categorias.yaml` | Definición de categorías de negocio con descripción, owner y criterios |
| `matriz-acceso.yaml` | Permisos: qué fuentes puede leer el agente y dónde están |
| `ingesta.md` | Plan de ingesta inicial e integración continua |

## Principios

1. **Un único documento fuente de verdad** — nunca duplicar contenido entre formatos
2. **Cada documento tiene un responsable** — sin owner, el documento se degrada
3. **Metadatos completos desde el día 1** — categoría, versión, vigencia, formato
4. **Ingesta automatizada** — el agente lee directo de la fuente, sin reenvíos manuales
5. **Calidad sobre cantidad** — solo documentos vigentes y aprobados entran a la base
