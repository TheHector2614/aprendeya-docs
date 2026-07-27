"""
Genera documentos HTML/HTML de muestra desde el contenido de src/content/docs.ts
para que el pipeline de ingesta tenga datos reales para procesar.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def extract_content_from_docs_ts() -> dict[str, str]:
    """Lee los contenidos de docs.ts y genera HTML."""
    docs_ts = ROOT / "src" / "content" / "docs.ts"
    content = docs_ts.read_text("utf-8")
    return content


def generate_html(title: str, sections: list[dict]) -> str:
    parts = [f"<html><body><h1>{title}</h1>"]
    for sec in sections:
        parts.append(f"<h2>{sec['title']}</h2>")
        for para in sec["content"].split("\n\n"):
            if para.strip():
                if para.startswith("- "):
                    parts.append("<ul>")
                    for line in para.split("\n"):
                        parts.append(f"<li>{line.replace('- ', '')}</li>")
                    parts.append("</ul>")
                else:
                    parts.append(f"<p>{para.strip()}</p>")
    parts.append("</body></html>")
    return "\n".join(parts)


def main():
    raw_dir = ROOT / "raw" / "web"
    raw_dir.mkdir(parents=True, exist_ok=True)

    inventario_path = ROOT / "docs-management" / "inventario.yaml"
    with open(inventario_path, "r", encoding="utf-8") as f:
        inventario = yaml.safe_load(f)["documentos"]

    # Contenido directamente desde las páginas HTML construidas
    docs_content = {
        "ACA-001": {
            "title": "Reglamento del Estudiante",
            "sections": [
                {"title": "Disposiciones Generales", "content": "El presente reglamento establece las normas que regulan la relación entre AprendeYa y sus estudiantes. Al inscribirse en cualquier curso o programa de la plataforma, el estudiante acepta de manera automática y voluntaria todas las disposiciones aquí contenidas.\n\nAprendeYa se reserva el derecho de modificar este reglamento en cualquier momento, notificando los cambios a los estudiantes a través del correo electrónico registrado o mediante anuncios en la plataforma con al menos quince días de antelación."},
                {"title": "De la Admisión y Matrícula", "content": "Para ser admitido como estudiante de AprendeYa, el aspirante debe completar el proceso de registro proporcionando información veraz y actualizada. La plataforma se reserva el derecho de verificar la identidad de los usuarios.\n\nLa matrícula se formaliza una vez realizado el pago correspondiente o, en el caso de programas de beca, una vez aprobada la solicitud.\n\nEl estudiante se compromete a:\n- No compartir sus credenciales de acceso con terceros\n- No redistribuir el contenido de los cursos\n- Utilizar la plataforma de manera ética y responsable"},
                {"title": "Derechos del Estudiante", "content": "Todo estudiante de AprendeYa tiene derecho a:\n- Acceder al contenido del curso durante el periodo de vigencia de su matrícula\n- Recibir retroalimentación oportuna sobre sus evaluaciones y proyectos\n- Solicitar certificados digitales al completar satisfactoriamente un curso\n- Participar en los foros y comunidades de aprendizaje\n- Solicitar soporte técnico y académico a través de los canales oficiales\n- Solicitar reembolso dentro de los términos establecidos\n- Que sus datos personales sean tratados conforme a la política de privacidad"},
                {"title": "Deberes y Obligaciones", "content": "Son deberes del estudiante:\n- Cumplir con las actividades académicas dentro de los plazos establecidos\n- Mantener una conducta respetuosa en foros, chats y espacios colaborativos\n- Reportar cualquier falla técnica o problema de acceso\n- Mantener actualizados sus datos de contacto\n- Respetar los derechos de autor y propiedad intelectual"},
                {"title": "Evaluación y Certificación", "content": "Cada curso establece sus propios criterios de evaluación. Para obtener la certificación, el estudiante debe:\n- Completar al menos el 80% de las actividades del curso\n- Obtener una calificación mínima de 70/100 en las evaluaciones finales\n- Entregar todos los proyectos requeridos dentro del plazo\n\nLos certificados digitales se emiten en un plazo máximo de 5 días hábiles."},
                {"title": "Faltas y Sanciones", "content": "Se consideran faltas graves:\n- Plagio o copia no autorizada de trabajos\n- Suplantación de identidad\n- Publicación de contenido ofensivo o ilegal\n- Intento de vulnerar la seguridad de la plataforma\n\nLas sanciones pueden incluir: amonestación por escrito, suspensión temporal, pérdida del derecho a certificación, o cancelación definitiva de la cuenta."},
            ],
        },
        "ACA-002": {
            "title": "Política de Reembolso de Matrículas",
            "sections": [
                {"title": "Condiciones Generales", "content": "En AprendeYa ofrecemos reembolsos bajo las condiciones descritas en esta política. Esta política aplica exclusivamente a cursos y programas pagados adquiridos directamente a través de la plataforma AprendeYa."},
                {"title": "Plazos de Reembolso", "content": "Cursos individuales: Puedes solicitar reembolso dentro de los primeros 7 días calendario desde la fecha de compra, siempre que no hayas avanzado más del 20% del contenido.\n\nProgramas completos: El plazo es de 14 días calendario con máximo de 15% de avance.\n\nPlanes de suscripción: Puedes cancelar en cualquier momento. El reembolso se calcula de forma proporcional.\n\nPaquetes de cursos: Aplica la misma política de los cursos individuales."},
                {"title": "Exclusiones", "content": "No procederán reembolsos en:\n- Cursos completados en más del 30%\n- Cursos adquiridos hace más de 30 días\n- Certificados o exámenes de certificación\n- Cursos con descuento superior al 50%\n- Programas con mentorías en vivo una vez iniciadas\n- Cuando se haya emitido el certificado del curso"},
                {"title": "Procedimiento de Solicitud", "content": "1. Inicia sesión en tu cuenta de AprendeYa\n2. Ve a Historial de Compras en la configuración de tu perfil\n3. Selecciona el curso\n4. Haz clic en Solicitar Reembolso\n5. Recibirás un correo de confirmación\n\nEl equipo revisará tu solicitud en un máximo de 5 días hábiles."},
                {"title": "Plazos de Devolución", "content": "Tarjeta de crédito/débito: 5 a 10 días hábiles\nPayPal: 2 a 5 días hábiles\nTransferencia bancaria: 3 a 7 días hábiles\nCrédito en la plataforma: 24 horas hábiles"},
            ],
        },
        "ACA-003": {
            "title": "Preguntas Frecuentes",
            "sections": [
                {"title": "Cursos y Contenido", "content": "¿Cómo elijo el curso adecuado para mí? Revisa la descripción de cada curso, los requisitos previos y el temario.\n\n¿Los cursos tienen horarios fijos? No. Todos nuestros cursos son asincrónicos.\n\n¿Cuánto tiempo tengo? Generalmente 6 meses para cursos individuales y 12 meses para programas completos."},
                {"title": "Certificados", "content": "¿Cómo obtengo mi certificado? Al completar todas las evaluaciones, descarga tu certificado desde Mis Logros.\n\n¿Los certificados tienen validez? Sí, incluyen un código de verificación único.\n\n¿Puedo recuperar un certificado perdido? Sí, están disponibles permanentemente en tu perfil."},
                {"title": "Pagos y Facturación", "content": "Aceptamos tarjetas de crédito y débito (Visa, Mastercard, American Express), PayPal y transferencias bancarias.\n\n¿Puedo pagar en cuotas? Sí, en cursos seleccionados.\n\n¿El precio incluye impuestos? Sí, los precios mostrados incluyen impuestos aplicables."},
                {"title": "Soporte Técnico", "content": "Escribe a soporte@aprendeya.com o usa el chat en vivo de lunes a viernes de 8:00 a 20:00 horas (GMT-5). Respondemos correos en máximo 24 horas hábiles."},
            ],
        },
        "ACA-004": {
            "title": "Guía de Uso de la Plataforma",
            "sections": [
                {"title": "Primeros Pasos", "content": "Creación de cuenta: Haz clic en Registrarse, completa tus datos y verifica tu correo.\n\nPerfil: Agrega tu foto, reseña profesional y áreas de interés para recibir recomendaciones personalizadas."},
                {"title": "Navegación Principal", "content": "Panel de control: Cursos en progreso, recomendaciones y actividad reciente.\n\nCatálogo de cursos: Filtra por categoría, nivel, duración e instructor.\n\nMis cursos: Organizados por estado: en progreso, completados y favoritos.\n\nComunidad: Foros, grupos de estudio y eventos en vivo."},
                {"title": "Reproducción de Contenido", "content": "Reproductor con controles de velocidad (0.5x a 2x), subtítulos, notas integradas, marcadores y transcripción completa."},
                {"title": "Seguimiento de Progreso", "content": "Barra de progreso visual, insignias y logros, estadísticas de aprendizaje y recomendaciones inteligentes basadas en tu historial."},
                {"title": "Herramientas Colaborativas", "content": "Foros de discusión por curso, grupos de estudio con chat y repositorio, mentorías premium y evaluación entre pares."},
            ],
        },
        "ACA-005": {
            "title": "Programa de Becas y Afiliados",
            "sections": [
                {"title": "Tipos de Beca", "content": "Beca al Mérito Académico: Cubre 50-100% del valor.\nBeca de Inclusión Digital: Acceso gratuito + subsidio de conectividad.\nBeca de Género en Tecnología: Cubre 80% de programas STEM.\nBeca de Emprendimiento: Cubre 60% del valor.\nBeca por Convenio Corporativo: Términos variables según el convenio."},
                {"title": "Requisitos y Postulación", "content": "Ser mayor de 16 años, contar con internet estable y completar el formulario.\n\nDocumentación requerida: certificados académicos, comprobante de comunidad, carta de motivación o resumen de proyecto según el tipo de beca."},
                {"title": "Proceso de Selección", "content": "Revisión documental (5 días), evaluación (10 días), entrevista si aplica, publicación de resultados. Convocatorias trimestrales."},
                {"title": "Programa de Afiliados", "content": "Comisiones: 20% por curso individual, 15% por programa completo, 10% recurrente por suscripción. Pagos mensuales con saldo mínimo de $50 USD."},
            ],
        },
    }

    for doc in inventario:
        doc_id = doc["id"]
        if doc_id not in docs_content:
            continue

        data = docs_content[doc_id]
        html = generate_html(data["title"], data["sections"])

        formato = doc.get("formato", "HTML").lower()
        if formato == "html":
            out = raw_dir / f"{doc_id}.html"
        elif formato == "md":
            out = raw_dir / f"{doc_id}.md"
        else:
            out = raw_dir / f"{doc_id}.html"

        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, "utf-8")
        print(f"  [generado] {out.relative_to(ROOT)}")

    print("\nMuestras generadas correctamente.")


if __name__ == "__main__":
    main()
