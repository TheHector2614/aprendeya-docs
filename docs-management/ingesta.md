# Plan de Ingesta Documental — AprendeYa

## Fase 1: Ingesta Inicial (manual + API)

### Objetivo
Incorporar los documentos existentes al pipeline de procesamiento del agente de IA. Esta fase combina carga manual para documentos estáticos (web) con conexiones API para fuentes dinámicas (Drive, SharePoint).

### Paso a paso

1. **Documentos del sitio web**
   - Ya están en HTML estático dentro del repositorio (`src/pages/`)
   - El agente puede leerlos directamente del sitio en producción
   - No requiere acción adicional de ingesta

2. **Google Drive**
   - Crear Service Account en Google Cloud Console
   - Compartir las carpetas relevantes con el email de la Service Account
   - Implementar script de ingesta usando `google-api-python-client`

3. **SharePoint**
   - Registrar App en Azure AD con permisos `Sites.Read.All`
   - Implementar script de ingesta usando Microsoft Graph API

4. **Repositorio GitHub**
   - Usar `gh` CLI o GitHub API con token existente
   - Clonar/docs/ o consumir vía API REST

5. **Correo electrónico**
   - Concesión de permisos delegados en Microsoft Graph
   - Filtrado de adjuntos por remitente/asunto

### Scripts de ingesta

```
scripts/
  ingest-drive.py      # Google Drive → raw/ 
  ingest-sharepoint.py  # SharePoint → raw/
  ingest-github.py      # GitHub docs → raw/
  ingest-mail.py        # Adjuntos de correo → raw/
```

Cada script:
- Descarga el documento a `raw/{categoria}/{id}/`
- Extrae metadatos (fecha, autor, versión)
- Registra la operación en el log de ingesta

---

## Fase 2: Integración Continua (automática)

### Objetivo
Mantener la base documental sincronizada sin intervención manual.

### Estrategia

| Fuente | Frecuencia | Método |
|---|---|---|
| Sitio web (HTML) | On push (CD) | Se regenera con Astro build |
| Google Drive | Diaria (cron) | Watch events + polling |
| SharePoint | Diaria (cron) | Delta query |
| GitHub | On push (webhook) | GitHub Actions trigger |
| Correo | Semanal (cron) | Polling con filtro de fecha |

### Webhooks / Triggers

```yaml
github:
  - evento: push
    rama: main
    acción: re-indexar docs técnicos de /docs/

google_drive:
  - evento: archivo modificado en carpeta RH/
    acción: re-indexar RH-001, RH-002

calendario:
  - frecuencia: diaria 06:00 UTC
    acción: sincronización completa de todas las fuentes
```

---

## Fase 3: Curaduría y Control de Versiones

### Flujo de actualización

1. El responsable de la categoría sube/actualiza un documento en su fuente original
2. El agente detecta el cambio (webhook o polling)
3. Descarga la nueva versión y la compara con la anterior (hash SHA-256)
4. Si cambió:
   - Incrementa el `version` en el inventario
   - Actualiza `vigencia` y opcionalmente `proxima_revision`
   - Mantiene la versión anterior en `archive/` con estado `OBS`
5. Notifica al responsable vía correo o Slack

### Política de retención

- **Documentos vigentes**: disponibles para búsqueda inmediata
- **Documentos obsoletos**: archivados con referencia al reemplazo
- **Borradores**: etiquetados como `BOR`, no indexados para búsqueda general
- **Duplicados**: se conserva el de mayor versión; el resto se marca como `OBS`

---

## Stack técnico sugerido para el pipeline

```
                     ┌─────────────────┐
                     │   Fuentes        │
                     │  (Drive, SPO,    │
                     │   GH, Web)       │
                     └────────┬────────┘
                              │
                     ┌────────▼────────┐
                     │  Scripts de     │
                     │  ingesta        │
                     │  (Python)       │
                     └────────┬────────┘
                              │
                     ┌────────▼────────┐
                     │  Almacenamiento │
                     │  raw/           │
                     │  (archivos)     │
                     └────────┬────────┘
                              │
                     ┌────────▼────────┐
                     │  Indexación     │
                     │  (embeddings)   │
                     └────────┬────────┘
                              │
                     ┌────────▼────────┐
                     │  Base Vectorial │
                     │  (búsqueda)     │
                     └────────┬────────┘
                              │
                     ┌────────▼────────┐
                     │  Agente IA      │
                     │  (respuestas)   │
                     └─────────────────┘
```
