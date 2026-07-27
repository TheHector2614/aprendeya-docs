from pathlib import Path
BASE = Path("raw")

# ── ACA-008 Guia del Instructor ──
html = """<html><body>
<h1>Guia del Instructor</h1>
<h2>Creacion de Cursos</h2>
<p>Para crear un curso, accede al Panel de Instructor desde tu perfil. Selecciona "Crear curso" y completa la informacion basica: titulo, descripcion, categoria, nivel, duracion estimada y requisitos previos. El curso quedara en estado "Borrador" hasta que lo envies a revision.</p>
<h2>Estructura del Curso</h2>
<p>Los cursos se organizan en modulos y cada modulo en lecciones. Cada leccion puede contener: video (max 20 min recomendado), texto enriquecido, presentaciones, archivos descargables y cuestionarios.</p>
<h2>Evaluacion de Estudiantes</h2>
<p>Puedes crear cuestionarios con preguntas de seleccion multiple, verdadero/falso, respuesta abierta y emparejamiento. La calificacion minima aprobatoria es 60/100. Los estudiantes ven su resultado inmediatamente despues de completar el cuestionario.</p>
<h2>Interaccion con Estudiantes</h2>
<p>Cada curso tiene un foro de preguntas y respuestas donde debes responder en un maximo de 48 horas habiles. Puedes programar sesiones en vivo usando la herramienta de videoconferencia integrada.</p>
<h2>Pagos para Instructores</h2>
<p>Los instructores reciben el 70% de los ingresos netos generados por sus cursos. Los pagos se realizan mensualmente via transferencia electronica, siempre que el saldo acumulado supere los $200 USD. El ciclo de pago cierra el dia 15 de cada mes.</p>
</body></html>"""
Path(BASE / "web" / "ACA-008.html").write_text(html, encoding="utf-8")
print("ACA-008.html OK")

# ── LEG-003 Propiedad Intelectual ──
html = """<html><body>
<h1>Politica de Propiedad Intelectual</h1>
<h2>Titularidad del Contenido</h2>
<p>El contenido creado por instructores en la plataforma AprendeYa es propiedad del instructor, quien concede a AprendeYa una licencia no exclusiva, mundial, libre de regalias, para alojar, distribuir y promocionar el contenido dentro de la plataforma.</p>
<h2>Contenido de Terceros</h2>
<p>Los instructores declaran y garantizan que todo el contenido publicado no infringe derechos de autor, marcas registradas ni cualquier otro derecho de propiedad intelectual de terceros.</p>
<h2>Uso por Parte de Estudiantes</h2>
<p>Los estudiantes adquieren una licencia personal, no transferible, para acceder al contenido de los cursos exclusivamente para su aprendizaje individual.</p>
<h2>Infracciones</h2>
<p>AprendeYa cuenta con un sistema de aviso y retirada. Si consideras que tu contenido ha sido utilizado de forma no autorizada, contacta a legal@aprendeya.com.</p>
<h2>Marca AprendeYa</h2>
<p>El nombre y logotipo de AprendeYa son marcas registradas. Su uso no autorizado requiere autorizacion previa por escrito del area de comunicaciones.</p>
</body></html>"""
Path(BASE / "web" / "LEG-003.html").write_text(html, encoding="utf-8")
print("LEG-003.html OK")

# ── LEG-005 Politica de Cookies ──
html = """<html><body>
<h1>Politica de Cookies</h1>
<h2>Que son las Cookies</h2>
<p>Las cookies son pequenos archivos de texto que se almacenan en tu dispositivo cuando visitas la plataforma AprendeYa. Utilizamos cookies propias y de terceros para garantizar el funcionamiento, analizar el uso y mejorar tu experiencia.</p>
<h2>Tipos de Cookies</h2>
<p>Cookies esenciales: necesarias para el funcionamiento basico (inicio de sesion, seguridad, idioma). No requieren consentimiento.</p>
<p>Cookies de rendimiento: informacion anonima sobre interaccion con la plataforma. Usamos Google Analytics y Hotjar.</p>
<p>Cookies de funcionalidad: recuerdan tus preferencias (idioma, moneda, ultimo curso visitado).</p>
<p>Cookies de publicidad: anuncios relevantes en plataformas de terceros (Meta, Google, TikTok).</p>
<h2>Gestion de Cookies</h2>
<p>Puedes aceptar, rechazar o configurar las cookies a traves del panel de preferencias en la parte inferior de cualquier pagina. Deshabilitar cookies esenciales puede afectar el funcionamiento de la plataforma.</p>
<h2>Cookies de Terceros</h2>
<p>Stripe (pagos), YouTube/Vimeo (videos), Meta Pixel (publicidad), Google Ads (publicidad), Google Analytics (analisis).</p>
</body></html>"""
Path(BASE / "web" / "LEG-005.html").write_text(html, encoding="utf-8")
print("LEG-005.html OK")

# ── ACA-009 Evaluacion y Calificaciones ──
html = """<html><body>
<h1>Politica de Evaluacion y Calificaciones</h1>
<h2>Sistema de Evaluacion</h2>
<p>La evaluacion se realiza a traves de cuestionarios, proyectos practicos, evaluaciones parciales y un examen final. Cada curso define los pesos especificos de cada componente.</p>
<h2>Escala de Calificacion</h2>
<p>Calificacion numerica de 0 a 100. Minimo aprobatorio: 60. Excelente: 90-100. Sobresaliente: 80-89. Aprobado: 60-79. Reprobado: 0-59.</p>
<h2>Intentos Permitidos</h2>
<p>Cuestionarios: hasta 3 intentos, se conserva la calificacion mas alta. Proyectos: permiten una reentrega si la calificacion es inferior a 60. Examen final: un unico intento.</p>
<h2>Apelaciones</h2>
<p>Puedes apelar dentro de los 5 dias habiles siguientes a la publicacion de la calificacion. El instructor tiene 10 dias habiles para responder.</p>
<h2>Honestidad Academica</h2>
<p>Prohibido: suplantacion, plagio, compartir respuestas de examenes, uso de IA no autorizado. Las violaciones resultan en anulacion del curso y posible suspension de la cuenta.</p>
</body></html>"""
Path(BASE / "web" / "ACA-009.html").write_text(html, encoding="utf-8")
print("ACA-009.html OK")

# ── ACA-010 Calendario Academico ──
html = """<html><body>
<h1>Calendario Academico 2026-2027</h1>
<h2>Periodos 2026</h2>
<p>Periodo 1 (ene-mar): Inscripciones 1-20 enero. Clases 27 ene - 21 mar. Evaluaciones 24-28 mar.</p>
<p>Periodo 2 (abr-jun): Inscripciones 1-20 abr. Clases 27 abr - 20 jun. Evaluaciones 23-27 jun.</p>
<p>Periodo 3 (jul-sep): Inscripciones 1-20 jul. Clases 27 jul - 19 sep. Evaluaciones 22-26 sep.</p>
<p>Periodo 4 (oct-dic): Inscripciones 1-20 oct. Clases 27 oct - 19 dic. Evaluaciones 22-26 dic.</p>
<h2>Feriados Colombia 2026</h2>
<p>Ene 1, Ene 12, Mar 23, Mar 27-28, May 1, May 18, Jun 8, Jun 15, Jun 29, Jul 20, Ago 7, Ago 17, Oct 12, Nov 2, Nov 16, Dic 8, Dic 25.</p>
<h2>Cursos Intensivos Verano 2027</h2>
<p>Enero 2027: 2 semanas (lun-sab, 4h diarias). Inscripciones abiertas desde el 1 de diciembre de 2026.</p>
<h2>Fechas Clave</h2>
<p>Ultimo dia reembolso total: 10 de enero. Certificaciones: primera semana de cada mes. Mantenimiento plataforma: ultimo sabado de cada mes 2am-6am.</p>
</body></html>"""
Path(BASE / "web" / "ACA-010.html").write_text(html, encoding="utf-8")
print("ACA-010.html OK")

# ── TEC-003 Manual de APIs y Webhooks ──
md = """# Manual de APIs y Webhooks

## Autenticacion

Todas las llamadas a la API requieren autenticacion mediante API Key en el header `X-API-Key`.

```
GET /api/v1/cursos
Host: api.aprendeya.com
X-API-Key: tu-api-key
Content-Type: application/json
```

## Endpoints Principales

### Cursos
- `GET /api/v1/cursos` - Listar cursos (paginado, 20 por pagina)
- `GET /api/v1/cursos/{id}` - Detalle de curso
- `POST /api/v1/cursos` - Crear curso (requiere rol instructor)
- `PUT /api/v1/cursos/{id}` - Actualizar curso
- `DELETE /api/v1/cursos/{id}` - Eliminar curso

### Estudiantes
- `GET /api/v1/estudiantes` - Listar estudiantes
- `GET /api/v1/estudiantes/{id}/progreso` - Progreso de un estudiante
- `POST /api/v1/estudiantes/{id}/certificado` - Generar certificado

### Pagos
- `GET /api/v1/pagos` - Historial de pagos
- `POST /api/v1/pagos/reembolso` - Solicitar reembolso

## Rate Limiting
- 1000 requests/minuto por API Key
- Respuesta 429 si se excede el limite
- Headers de rate limit incluidos en cada respuesta

## Webhooks

### Eventos Disponibles
- `curso.creado` - Se creo un nuevo curso
- `curso.actualizado` - Se actualizo un curso existente
- `estudiante.inscrito` - Un estudiante se inscribio a un curso
- `estudiante.completado` - Un estudiante completo un curso
- `pago.exitosa` - Pago procesado exitosamente
- `pago.reembolsado` - Reembolso procesado

### Configuracion
Registra tu URL de webhook en el panel de desarrollador. La plataforma enviara un POST con el payload del evento. Debes responder con 200 OK dentro de 5 segundos. La plataforma reintenta hasta 3 veces con backoff exponencial.
"""
Path(BASE / "github" / "TEC-003.md").write_text(md, encoding="utf-8")
print("TEC-003.md OK")

# ── TEC-004 Politica de Seguridad Informatica ──
md = """# Politica de Seguridad Informatica

## Controles de Acceso
- Autenticacion multifactor (MFA) obligatoria para todos los colaboradores
- Principio de minimo privilegio: acceso solo a los recursos necesarios
- Revision trimestral de accesos y permisos
- Cuentas de servicio rotan contrasenas cada 90 dias

## Gestion de Parches
- Parches de seguridad criticos: aplicar en menos de 48 horas
- Parches de alta prioridad: aplicar en menos de 7 dias
- Parches de media/baja prioridad: aplicar en el ciclo mensual
- Escaneo de vulnerabilidades semanal con Trivy y Snyk

## Proteccion de Datos
- Cifrado AES-256 en reposo para todas las bases de datos
- Cifrado TLS 1.3 en transito para todas las comunicaciones
- Backups diarios con retencion de 30 dias
- Pruebas de restauracion mensuales

## Seguridad de Red
- Firewalls de aplicacion web (WAF) en todos los endpoints
- Segmentacion de red por ambiente (dev/staging/prod)
- VPN obligatoria para acceso a recursos internos
- Monitoreo de trafico con deteccion de intrusiones (IDS)

## Dispositivos
- Dispositivos corporativos: administrados via MDM con cifrado de disco
- Politica de pantalla bloqueada (maximo 5 minutos de inactividad)
- Prohibido conectar dispositivos de almacenamiento no autorizados
- Todos los equipos deben tener antivirus actualizado
"""
Path(BASE / "github" / "TEC-004.md").write_text(md, encoding="utf-8")
print("TEC-004.md OK")

# ── TEC-005 Estandares de Codigo ──
md = """# Guia de Estandares de Codigo

## Convenciones Generales
- Lenguaje: Python 3.12+, TypeScript 5.x, Java 21
- Estilo: Ruff (Python), ESLint (TypeScript), Checkstyle (Java)
- Formato: Ruff format (Python), Prettier (TypeScript)
- Tabulacion: 4 espacios (Python), 2 espacios (TypeScript)

## Branching Strategy
- `main` - produccion, solo merge via PR aprobado
- `develop` - integracion, branch base para features
- `feature/{nombre}` - nuevas funcionalidades, basadas en develop
- `fix/{nombre}` - correcciones, basadas en develop
- `hotfix/{nombre}` - correcciones urgentes, basadas en main

## Code Review
- Todo cambio debe pasar por PR con al menos 1 approval
- El PR debe incluir tests que pasen en CI
- Prohibido mergear PR propio sin approval
- Maximo 400 lineas por PR (excepciones documentadas)

## Commits
- Prefijos: feat, fix, chore, docs, refactor, test, style
- Formato: `tipo(scope): mensaje en ingles imperativo`
- Ejemplo: `feat(courses): add search by category endpoint`

## Testing
- Cobertura minima: 80% (unit), 60% (integration)
- Tests unitarios obligatorios para toda logica de negocio
- Tests de integracion para endpoints de API
- E2E para flujos criticos (login, checkout, certificacion)
"""
Path(BASE / "github" / "TEC-005.md").write_text(md, encoding="utf-8")
print("TEC-005.md OK")

print("\nTodos los HTML y MD OK")
