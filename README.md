# AprendeYa — Documentación Corporativa

Sitio web estático que presenta la documentación oficial de **AprendeYa**, una plataforma educativa ficticia. Construido como parte del **Challenge ONE Alura — IA para Tech**.

## Tecnologías

- **Astro 6** — generación de sitio estático
- **React 19** — componentes interactivos
- **Tailwind CSS 4** — estilos utilitarios
- **TypeScript** — tipado estático

## Páginas

| Ruta | Documento |
|---|---|
| `/` | Landing con tarjetas de acceso |
| `/reglamento-estudiante` | Reglamento del Estudiante |
| `/politica-reembolso` | Política de Reembolso de Matrículas |
| `/faq` | Preguntas Frecuentes (FAQ) |
| `/guia-uso` | Guía de Uso de la Plataforma |
| `/programa-becas` | Programa de Becas y Afiliados |

## Cómo ejecutar

```bash
npm install
npm run dev      # desarrollo en http://localhost:4321
npm run build    # generar sitio estático en dist/
npm run preview  # previsualizar el build
```

## Contenido

Los 5 documentos contienen contenido ficticio generado con IA, incluyendo:
- Reglamento académico (admisión, derechos, deberes, sanciones)
- Política de reembolsos (plazos, exclusiones, procedimiento)
- FAQ (cursos, certificados, pagos, soporte)
- Guía de plataforma (primeros pasos, navegación, herramientas)
- Programa de becas y afiliados (tipos, requisitos, comisiones)

## Gestión Documental

El proyecto incluye un sistema completo de organización documental en `docs-management/`:

| Archivo | Propósito |
|---|---|
| `inventario.yaml` | Registro maestro con metadatos de todos los documentos |
| `categorias.yaml` | Definición de 8 categorías de negocio con responsables |
| `matriz-acceso.yaml` | Fuentes, métodos de conexión y permisos del agente |
| `ingesta.md` | Plan de ingesta inicial e integración continua |

### Pipeline de Procesamiento (Etapa 2)

El directorio `scripts/` contiene el pipeline de procesamiento e indexación semántica:

```
scripts/
├── pipeline/
│   ├── extractor.py    # Extrae texto de HTML, DOCX, XLSX, MD, TXT
│   ├── chunker.py      # Divide documentos en chunks con overlap
│   ├── embedder.py     # Genera embeddings multilingües (sentence-transformers)
│   └── indexer.py      # Indexa en ChromaDB (búsqueda por similitud coseno)
├── ingest.py           # Ingesta completa desde inventario.yaml
├── search.py           # Búsqueda semántica por consola
├── generate_samples.py # Genera documentos de muestra
└── requirements.txt
```

**Uso:**
```bash
cd scripts
pip install -r requirements.txt
python generate_samples.py   # genera docs de muestra en raw/
python ingest.py             # extrae → chunk → embed → indexar
python search.py "mi consulta" --top-k 3
```

### Estructura del pipeline

```
Etapa 1  →  Recolección y Organización  (docs-management/)    ✓
Etapa 2  →  Procesamiento e Indexación  (scripts/ + index/)   ✓
Etapa 3  →  Búsqueda y Generación de Respuestas                ← SIGUIENTE
```

## Requisitos

- **Node.js 18+** — para el sitio web
- **Python 3.10+** — para el pipeline de procesamiento
