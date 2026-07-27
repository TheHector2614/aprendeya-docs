export interface DocSection {
  title: string
  content: string
}

export interface DocPage {
  id: string
  title: string
  description: string
  icon: string
  iconName: string
  category: string
  badge: string
  readTime: string
  sections: DocSection[]
}

export const docs: DocPage[] = [
  {
    id: "reglamento-estudiante",
    title: "Reglamento del Estudiante",
    description: "Conoce las normas, derechos y deberes que rigen la relación académica en AprendeYa.",
    icon: "📜",
    iconName: "ScrollText",
    category: "Normativa Académica",
    badge: "Oficial",
    readTime: "7 min de lectura",
    sections: [
      {
        title: "Disposiciones Generales",
        content: `El presente reglamento establece las normas que regulan la relación entre AprendeYa y sus estudiantes. Al inscribirse en cualquier curso o programa de la plataforma, el estudiante acepta de manera automática y voluntaria todas las disposiciones aquí contenidas.

AprendeYa se reserva el derecho de modificar este reglamento en cualquier momento, notificando los cambios a los estudiantes a través del correo electrónico registrado o mediante anuncios en la plataforma con al menos quince (15) días de antelación.`,
      },
      {
        title: "De la Admisión y Matrícula",
        content: `Para ser admitido como estudiante de AprendeYa, el aspirante debe completar el proceso de registro proporcionando información veraz y actualizada. La plataforma se reserva el derecho de verificar la identidad de los usuarios y de rechazar solicitudes que contengan información falsa o incompleta.

La matrícula se formaliza una vez realizado el pago correspondiente o, en el caso de programas de beca, una vez aprobada la solicitud. Cada curso tiene una duración definida y el acceso al contenido se otorga por el periodo establecido en la descripción del curso.

El estudiante se compromete a:
- No compartir sus credenciales de acceso con terceros
- No redistribuir el contenido de los cursos
- Utilizar la plataforma de manera ética y responsable`,
      },
      {
        title: "Derechos del Estudiante",
        content: `Todo estudiante de AprendeYa tiene derecho a:
- Acceder al contenido del curso durante el periodo de vigencia de su matrícula
- Recibir retroalimentación oportuna sobre sus evaluaciones y proyectos
- Solicitar certificados digitales al completar satisfactoriamente un curso
- Participar en los foros y comunidades de aprendizaje
- Solicitar soporte técnico y académico a través de los canales oficiales
- Solicitar reembolso dentro de los términos establecidos en la política de reembolsos
- Que sus datos personales sean tratados conforme a la política de privacidad de la plataforma`,
      },
      {
        title: "Deberes y Obligaciones",
        content: `Son deberes del estudiante:
- Cumplir con las actividades académicas dentro de los plazos establecidos
- Mantener una conducta respetuosa en foros, chats y espacios colaborativos
- Reportar cualquier falla técnica o problema de acceso al equipo de soporte
- Mantener actualizados sus datos de contacto
- Respetar los derechos de autor y propiedad intelectual del contenido

El incumplimiento reiterado de estos deberes podrá dar lugar a la suspensión temporal o definitiva de la cuenta del estudiante, sin derecho a reembolso.`,
      },
      {
        title: "Evaluación y Certificación",
        content: `Cada curso establece sus propios criterios de evaluación, los cuales son comunicados al estudiante al inicio del curso. Para obtener la certificación, el estudiante debe:
- Completar al menos el 80% de las actividades del curso
- Obtener una calificación mínima de 70/100 en las evaluaciones finales
- Entregar todos los proyectos requeridos dentro del plazo

Los certificados digitales se emiten en un plazo máximo de 5 días hábiles después de completar el curso. Estos certificados incluyen un código de verificación único que permite validar su autenticidad.`,
      },
      {
        title: "Faltas y Sanciones",
        content: `Se consideran faltas graves:
- Plagio o copia no autorizada de trabajos de otros estudiantes
- Suplantación de identidad
- Publicación de contenido ofensivo, discriminatorio o ilegal en los foros
- Intento de vulnerar la seguridad de la plataforma
- Venta o comercialización no autorizada de cursos o certificados

Las sanciones pueden incluir: amonestación por escrito, suspensión temporal del acceso, pérdida del derecho a certificación, o cancelación definitiva de la cuenta. La gravedad de la sanción será determinada por el comité académico de AprendeYa.`,
      },
    ],
  },
  {
    id: "guia-uso",
    title: "Guía de Uso de la Plataforma",
    description: "Aprende a navegar por AprendeYa: desde tu primer registro hasta el seguimiento de tu progreso académico.",
    icon: "📖",
    iconName: "BookOpen",
    category: "Tutoriales y Guías",
    badge: "Esencial",
    readTime: "6 min de lectura",
    sections: [
      {
        title: "Primeros Pasos",
        content: `Bienvenido a AprendeYa. Esta guía te ayudará a aprovechar al máximo todas las funcionalidades de nuestra plataforma educativa.

Creación de cuenta: Para comenzar, haz clic en "Registrarse" en la esquina superior derecha. Completa tus datos personales, incluyendo nombre completo, correo electrónico y una contraseña segura. Recibirás un correo de verificación; haz clic en el enlace para activar tu cuenta.

Perfil de estudiante: Una vez verificada tu cuenta, completa tu perfil agregando tu foto, una breve reseña profesional, y tus áreas de interés. Esto nos permite recomendarte cursos relevantes.`,
      },
      {
        title: "Navegación Principal",
        content: `La plataforma está organizada en las siguientes secciones principales:

Panel de control: Tu página de inicio personalizada donde encuentras tus cursos en progreso, recomendaciones y actividad reciente.

Catálogo de cursos: Explora todos los cursos disponibles. Puedes filtrar por categoría, nivel de dificultad, duración e instructor. Cada curso tiene una página de detalle con temario, requisitos y reseñas.

Mis cursos: Aquí encuentras todos los cursos en los que estás inscrito, organizados por estado: en progreso, completados y favoritos.

Comunidad: Accede a los foros de discusión, grupos de estudio y eventos en vivo programados.

Calendario: Visualiza las fechas importantes: entregas de proyectos, sesiones en vivo y fechas límite.`,
      },
      {
        title: "Reproducción de Contenido",
        content: `Los cursos utilizan un reproductor de video interactivo con las siguientes funcionalidades:

- Controles de velocidad: 0.5x, 1x, 1.25x, 1.5x y 2x
- Subtítulos automáticos en español e inglés
- Notas integradas: toma notas sincronizadas con el video
- Marcadores: guarda momentos importantes del video
- Transcripción completa del contenido audiovisual

Junto al reproductor, encontrarás los materiales complementarios: PDFs, enlaces, ejercicios prácticos y quizzes de verificación.`,
      },
      {
        title: "Seguimiento de Progreso",
        content: `AprendeYa cuenta con un sistema integral de seguimiento de progreso:

Barra de progreso: Cada curso muestra visualmente tu avance general. Al completar una lección, el progreso se actualiza automáticamente.

Insignias y logros: Al alcanzar hitos importantes (primer curso completado, racha de estudio, participación en foros), recibirás insignias que se muestran en tu perfil.

Estadísticas de aprendizaje: La sección "Mis Estadísticas" te muestra horas de estudio, cursos completados, promedio de calificaciones y tu racha actual de días consecutivos de estudio.

Recomendaciones inteligentes: Basado en tu historial de aprendizaje, la plataforma te sugiere cursos complementarios para profundizar en tus áreas de interés.`,
      },
      {
        title: "Herramientas Colaborativas",
        content: `AprendeYa fomenta el aprendizaje colaborativo a través de:

Foros de discusión: Cada curso tiene su propio foro donde puedes publicar preguntas, compartir conocimientos y resolver dudas con compañeros e instructores.

Grupos de estudio: Crea o únete a grupos de estudio para trabajar en proyectos colaborativos. Los grupos tienen su propio espacio de chat y repositorio de archivos.

Mentorías: En programas premium, puedes agendar sesiones individuales con mentores para recibir retroalimentación personalizada sobre tus proyectos.

Evaluación entre pares: Algunos cursos incluyen actividades donde puedes revisar y retroalimentar los trabajos de otros estudiantes, desarrollando tu capacidad crítica y analítica.`,
      },
    ],
  },
  {
    id: "programa-becas",
    title: "Programa de Becas y Afiliados",
    description: "Descubre las oportunidades de becas disponibles y cómo puedes ganar dinero recomendando AprendeYa.",
    icon: "🎓",
    iconName: "GraduationCap",
    category: "Oportunidades",
    badge: "Convocatoria Abierta",
    readTime: "8 min de lectura",
    sections: [
      {
        title: "Tipos de Beca",
        content: `AprendeYa ofrece diversas modalidades de beca para garantizar que el acceso a la educación de calidad sea inclusivo y equitativo:

Beca al Mérito Académico: Otorgada a estudiantes con promedio sobresaliente en su formación previa. Cubre entre el 50% y el 100% del valor del curso.

Beca de Inclusión Digital: Dirigida a personas de comunidades con acceso limitado a recursos tecnológicos. Incluye acceso gratuito al curso más un subsidio para conectividad.

Beca de Género en Tecnología: Orientada a promover la participación de mujeres y personas no binarias en áreas STEM. Cubre el 80% del valor de programas tecnológicos.

Beca de Emprendimiento: Para emprendedores que deseen adquirir habilidades para impulsar sus proyectos. Cubre el 60% del valor del curso.

Beca por Convenio Corporativo: Disponible para empleados de empresas aliadas de AprendeYa. Los términos varían según el convenio específico.`,
      },
      {
        title: "Requisitos y Postulación",
        content: `Los requisitos generales para aplicar a una beca son:

- Ser mayor de 16 años
- Contar con conexión a internet estable
- Completar el formulario de postulación con la documentación requerida
- Demostrar el interés y la motivación para completar el programa

Documentación requerida según el tipo de beca:
- Mérito académico: certificados de notas o títulos
- Inclusión digital: comprobante de pertenencia a comunidad objetivo
- Género: carta de motivación personal
- Emprendimiento: resumen del proyecto emprendedor

Las convocatorias se abren trimestralmente. Puedes consultar las fechas en la sección "Becas" de nuestra plataforma.`,
      },
      {
        title: "Proceso de Selección",
        content: `El proceso de selección consta de las siguientes etapas:

1. Revisión documental (5 días hábiles): Verificación de que la postulación cumple con los requisitos mínimos.

2. Evaluación de la solicitud (10 días hábiles): Análisis detallado de cada postulación por parte del comité de becas.

3. Entrevista (si aplica): Para becas de alto valor o programas específicos, se realiza una entrevista virtual.

4. Publicación de resultados: Los resultados se publican en la plataforma y se notifican por correo electrónico.

El comité de becas está conformado por miembros del equipo académico y representantes de las comunidades aliadas. Las decisiones del comité son inapelables.`,
      },
      {
        title: "Condiciones de Renovación",
        content: `Las becas están sujetas a renovación periódica según las siguientes condiciones:

- Mantener un promedio mínimo de 75/100 en las evaluaciones
- Completar al menos el 70% de las actividades dentro del período establecido
- Participar activamente en al menos un foro o grupo de estudio por mes
- No haber incurrido en faltas disciplinarias graves

En caso de no cumplir con estas condiciones, la beca podrá ser reducida o cancelada. El estudiante será notificado con 15 días de antelación y tendrá derecho a presentar una apelación.`,
      },
      {
        title: "Programa de Afiliados",
        content: `El Programa de Afiliados de AprendeYa te permite ganar dinero recomendando nuestros cursos a tu red de contactos.

¿Cómo funciona? Al registrarte como afiliado, recibes un enlace único de referencia. Cuando alguien realiza una compra a través de tu enlace, recibes una comisión.

Comisiones:
- Curso individual: 20% del valor de la venta
- Programa completo: 15% del valor de la venta
- Suscripción: 10% recurrente durante los primeros 6 meses del referido

Requisitos para ser afiliado:
- Ser mayor de edad
- Tener presencia en redes sociales o sitio web
- No utilizar publicidad engañosa ni spam

Los pagos se realizan mensualmente, siempre que el saldo acumulado sea superior a $50 USD. El programa es acumulable con otras promociones y no tiene límite de referidos.`,
      },
      {
        title: "Preguntas Frecuentes sobre Becas",
        content: `¿Puedo aplicar a más de una beca?
No. Solo puedes postularte a un tipo de beca por convocatoria. Si no resultas seleccionado, puedes aplicar a otra en la siguiente convocatoria.

¿La beca cubre la certificación?
Sí, las becas incluyen el certificado digital al completar satisfactoriamente el curso.

¿Puedo combinar una beca con otra promoción?
No. Las becas no son acumulables con otros descuentos o promociones.

¿Cuánto tiempo dura el proceso de selección?
El proceso completo tiene una duración aproximada de 20 a 25 días hábiles desde el cierre de la convocatoria.

Si tienes más dudas, escríbenos a becas@aprendeya.com.`,
      },
    ],
  },
  {
    id: "politica-reembolso",
    title: "Política de Reembolso de Matrículas",
    description: "Consulta las condiciones, plazos y procedimiento para solicitar la devolución de tu inversión educativa.",
    icon: "💳",
    iconName: "CreditCard",
    category: "Facturación y Garantía",
    badge: "Financiero",
    readTime: "5 min de lectura",
    sections: [
      {
        title: "Condiciones Generales",
        content: `En AprendeYa queremos que estés completamente satisfecho con tu experiencia de aprendizaje. Por ello, ofrecemos reembolsos bajo las condiciones descritas en esta política.

Esta política aplica exclusivamente a cursos y programas pagados adquiridos directamente a través de la plataforma AprendeYa. No aplica para compras realizadas a través de terceros o programas gratuitos.`,
      },
      {
        title: "Plazos de Reembolso",
        content: `El plazo para solicitar reembolso varía según el tipo de programa:

Cursos individuales: Puedes solicitar reembolso dentro de los primeros 7 días calendario desde la fecha de compra, siempre que no hayas avanzado más del 20% del contenido del curso.

Programas completos (bootcamps, diplomados): El plazo de reembolso es de 14 días calendario desde la fecha de inscripción, con un máximo de 15% de avance en el contenido total del programa.

Planes de suscripción: Puedes cancelar tu suscripción en cualquier momento. El reembolso se calcula de forma proporcional a los días restantes del período de facturación actual.

Paquetes de cursos: Aplica la misma política de los cursos individuales, calculada desde la fecha de compra del paquete.`,
      },
      {
        title: "Exclusiones",
        content: `No procederán reembolsos en los siguientes casos:
- Cursos completados en más del 30%
- Cursos adquiridos hace más de 30 días
- Certificados o exámenes de certificación
- Cursos comprados durante promociones especiales con descuento superior al 50%
- Programas que incluyan mentorías en vivo una vez iniciadas
- Cursos regalados o transferidos a otro usuario
- Cuando se haya emitido el certificado del curso`,
      },
      {
        title: "Procedimiento de Solicitud",
        content: `Para solicitar un reembolso, sigue estos pasos:

1. Inicia sesión en tu cuenta de AprendeYa
2. Ve a "Historial de Compras" en la configuración de tu perfil
3. Selecciona el curso o programa para el cual deseas solicitar reembolso
4. Haz clic en "Solicitar Reembolso" y completa el formulario indicando el motivo
5. Recibirás un correo de confirmación con el número de solicitud

El equipo de soporte revisará tu solicitud en un plazo máximo de 5 días hábiles y te notificará la decisión por correo electrónico.`,
      },
      {
        title: "Plazos de Devolución",
        content: `Una vez aprobada la solicitud de reembolso, los plazos de devolución son:

- Tarjeta de crédito/débito: 5 a 10 días hábiles (dependiendo del banco emisor)
- PayPal: 2 a 5 días hábiles
- Transferencia bancaria: 3 a 7 días hábiles
- Crédito en la plataforma: 24 horas hábiles

El reembolso se realiza por el mismo medio de pago utilizado en la compra original. En caso de que el medio de pago original ya no esté disponible, el reembolso se realizará como crédito en la plataforma.`,
      },
    ],
  },
  {
    id: "faq",
    title: "Preguntas Frecuentes",
    description: "Respuestas a las dudas más comunes sobre cursos, certificados, pagos y soporte técnico.",
    icon: "❓",
    iconName: "HelpCircle",
    category: "Soporte General",
    badge: "Soporte 24/7",
    readTime: "5 min de lectura",
    sections: [
      {
        title: "Cursos y Contenido",
        content: `¿Cómo elijo el curso adecuado para mí?
Revisa la descripción de cada curso, los requisitos previos y el temario. También puedes contactar a nuestro equipo de asesoría académica para recibir recomendaciones personalizadas.

¿Los cursos tienen horarios fijos?
No. Todos nuestros cursos son asincrónicos, lo que significa que puedes estudiar a tu propio ritmo, las 24 horas del día, los 7 días de la semana. Algunos programas incluyen sesiones en vivo opcionales.

¿Cuánto tiempo tengo para completar un curso?
Depende del curso. Generalmente, los cursos individuales tienen acceso por 6 meses, los programas completos por 12 meses, y las suscripciones mantienen acceso mientras estén activas.

¿Puedo acceder al contenido después de completar el curso?
Sí, mantienes acceso al material del curso por 3 meses adicionales después de completarlo. En programas completos, el acceso se extiende a 6 meses.`,
      },
      {
        title: "Certificados",
        content: `¿Cómo obtengo mi certificado?
Al completar satisfactoriamente todas las evaluaciones y proyectos del curso, encontrarás la opción de descargar tu certificado desde la sección "Mis Logros" en tu perfil.

¿Los certificados tienen validez?
Sí, nuestros certificados incluyen un código de verificación único que permite a empleadores e instituciones educativas validar su autenticidad a través de nuestra plataforma.

¿Puedo compartir mi certificado en LinkedIn?
Sí. Desde la sección de certificados puedes generar un enlace público para compartir en LinkedIn, tu portafolio o currículum.

¿Puedo recuperar un certificado perdido?
Sí. Los certificados están disponibles permanentemente en tu perfil de AprendeYa. Puedes descargarlos nuevamente en cualquier momento desde "Mis Logros".`,
      },
      {
        title: "Pagos y Facturación",
        content: `¿Qué métodos de pago aceptan?
Aceptamos tarjetas de crédito y débito (Visa, Mastercard, American Express), PayPal, y transferencias bancarias en algunos países de Latinoamérica.

¿Puedo pagar en cuotas?
Sí, ofrecemos opciones de pago fraccionado en cursos seleccionados. Las opciones de cuotas se muestran durante el proceso de pago.

¿Emite factura o recibo?
Sí, generamos factura electrónica con validez fiscal para todos los pagos realizados. Puedes descargarla desde la sección "Historial de Compras".

¿El precio incluye impuestos?
Los precios mostrados incluyen los impuestos aplicables según la legislación del país del estudiante.`,
      },
      {
        title: "Soporte Técnico",
        content: `¿Qué hago si no puedo acceder a mi curso?
Primero, verifica tu conexión a internet. Si el problema persiste, cierra sesión y vuelve a iniciarla. Si aún así no funciona, contacta a nuestro soporte técnico.

¿Cómo contacto al soporte?
Puedes escribirnos a soporte@aprendeya.com o usar el chat en vivo disponible en la plataforma de lunes a viernes de 8:00 a 20:00 horas (GMT-5).

¿En qué horario responden?
Respondemos correos electrónicos en un máximo de 24 horas hábiles. El chat en vivo tiene atención en tiempo real durante el horario indicado.

¿Ofrecen soporte en varios idiomas?
Sí, ofrecemos soporte en español, inglés y portugués.`,
      },
    ],
  },
]
