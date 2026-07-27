# 🎓 AprendeYa — Centro de Documentación Oficial e Inteligente

> **Plataforma Educativa de Vanguardia** con Asistente Virtual de Inteligencia Artificial (IA RAG), Buscador Modal Instantáneo `Ctrl + K`, Tabla de Contenidos con ScrollSpy y un Sistema de Diseño Glassmorphism de Alta Fidelidad Estética.

Desarrollado como parte del **Challenge ONE Alura — IA para Tech**.

---

## 🌟 Características Principales

### 🤖 Asistente Virtual de IA Integrado (`AIChatWidget.astro`)
- **Atención 24/7 en tiempo real**: Botón flotante animado con respuestas enriquecidas sobre becas, reglamentos, reembolsos y guías de uso.
- **Sugerencias de inicio rápido**: Chips interactivos para preguntas comunes.
- **Citas con un clic**: Respuestas estructuradas con enlaces directos a las cláusulas oficiales.

### 🔍 Buscador Modal Instantáneo `Ctrl + K` (`SearchModal.astro`)
- Búsqueda en tiempo real sobre títulos, descripciones y contenido de secciones.
- Navegación fluida por teclado (`↑`, `↓`, `Enter`, `ESC`).

### 📖 Experiencia de Lectura Avanzada
- **Tabla de Contenidos (TOC)**: Seguimiento dinámico de la sección activa (*ScrollSpy*) y acordeón desplegable responsivo para dispositivos móviles.
- **Barra de Progreso de Lectura**: Indicador visual superior que se llena al desplazarse.
- **Formateador de Texto (`DocRenderer.astro`)**: Separación inteligente de párrafos, listas con viñetas esféricas únicas y cajas de llamada (*callouts*).
- **Indicadores y Metadatos**: Tiempo estimado de lectura por documento y etiquetas de categoría (*Oficial*, *Financiero*, *Esencial*, *Convocatoria Abierta*).

### 🎨 Diseño Responsivo y Glassmorphism
- Encabezado translúcido con desenfoque de fondo (`backdrop-filter blur-md`).
- Menú lateral (*Sidebar*) responsivo con cortina de fondo (*backdrop overlay*) en móviles.
- Tipografía moderna con **Plus Jakarta Sans** (títulos), **Inter** (cuerpo) y **JetBrains Mono** (código).

---

## 🛠️ Stack Tecnológico

| Capa | Tecnología | Propósito |
|---|---|---|
| **Frontend Framework** | **Astro 6** | Generación de sitio estático ultrarrápido |
| **Estilos & UI** | **Tailwind CSS 4** | Sistema de diseño utilitario y animaciones |
| **Iconografía** | **Lucide Icons** | Iconografía vectorial coherente |
| **Lenguaje** | **TypeScript / JavaScript** | Tipado y lógica interactiva client-side |
| **RAG Pipeline** | **Python 3.10+ / FastAPI** | API de recuperación e indexación semántica |
| **Embeddings & Vector Database** | **Sentence-Transformers & ChromaDB** | Búsqueda por similitud vectorial |
| **Despliegue OCI** | **Docker & OCI Container Instances** | Contenedores e infraestructura cloud |

---

## 🗺️ Mapa de Páginas y Rutas

| Ruta | Documento | Categoría | Insignia |
|---|---|---|---|
| `/` | **Inicio / Catálogo General** | Landing Principal | `Centro Oficial` |
| `/reglamento-estudiante` | **Reglamento del Estudiante** | Normativa Académica | `Oficial` |
| `/guia-uso` | **Guía de Uso de la Plataforma** | Tutoriales y Guías | `Esencial` |
| `/programa-becas` | **Programa de Becas y Afiliados** | Oportunidades | `Convocatoria Abierta` |
| `/politica-reembolso` | **Política de Reembolso de Matrículas** | Facturación y Garantía | `Financiero` |
| `/faq` | **Preguntas Frecuentes (FAQ)** | Soporte General | `Soporte 24/7` |

---

## 🚀 Inicio Rápido

### Prerrequisitos
- **Node.js 18+**
- **npm** o **pnpm**

### Instalación y Desarrollo Frontend

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/aprendeya-docs.git
cd aprendeya-docs

# 2. Instalar dependencias
npm install

# 3. Iniciar el servidor de desarrollo
npm run dev
```

El sitio estará disponible en [http://localhost:4321](http://localhost:4321).

### Comandos de Compilación

```bash
# Generar la versión estática de producción
npm run build

# Previsualizar el sitio de producción compilado
npm run preview
```

---

## 🤖 Pipeline de Ingesta y Agente RAG (Python)

El proyecto cuenta con una infraestructura RAG completa ubicada en `scripts/`:

```
scripts/
├── pipeline/
│   ├── extractor.py    # Extrae texto de HTML, DOCX, XLSX, MD, TXT
│   ├── chunker.py      # Divide documentos en fragmentos con overlap
│   ├── embedder.py     # Genera embeddings multilingües (Sentence-Transformers)
│   ├── indexer.py      # Indexa vectores en ChromaDB
│   └── agent.py        # Agente RAG: recupera contexto y redacta respuestas
├── ingest.py           # Ingesta completa desde docs-management/inventario.yaml
├── api.py              # Servicio REST FastAPI (POST /ask)
└── chat.html           # Interfaz web independiente de pruebas
```

### Ejecutar el Servidor RAG Backend

```bash
cd scripts
pip install -r requirements.txt
python ingest.py        # Ingestar e indexar documentos
python api.py           # Servir API REST en http://localhost:8000
```

---

## 📁 Gestión Documental y Despliegue en la Nube

- **Gestión Documental**: Matriz de acceso, inventario maestro y flujo de ingesta en [`docs-management/`](file:///d:/Documentos/CARPETA%20IMPORTANTE/PROGRAMACION/OTROS%20PROGRAMAS/Proyectos/aprendeya-docs/docs-management/).
- **Despliegue OCI (Oracle Cloud Infrastructure)**: Configuración Docker, scripts de despliegue y guía paso a paso en [`oci/`](file:///d:/Documentos/CARPETA%20IMPORTANTE/PROGRAMACION/OTROS%20PROGRAMAS/Proyectos/aprendeya-docs/oci/README.md).

---

## 📜 Licencia y Créditos

Este proyecto forma parte del **Challenge ONE Alura — IA para Tech**.  
Todos los derechos reservados © {new Date().getFullYear()} **AprendeYa Inc.**
