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

### Estructura del pipeline

```
Etapa 1  →  Recolección y Organización  (docs-management/)    ← HECHO
Etapa 2  →  Procesamiento e Indexación
Etapa 3  →  Búsqueda y Generación de Respuestas
```
