import logging
import warnings

from .config import Config
from .embedder import Embedder
from .indexer import Indexer
from .generator import Generator

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("agent")
warnings.filterwarnings("ignore", category=UserWarning, module="huggingface_hub")


class Agent:
    def __init__(self):
        self.cfg = Config()
        self.embedder = Embedder(model_name=self.cfg.EMBEDDING_MODEL)
        self.indexer = Indexer(
            persist_dir=str(self.cfg.INDEX_DIR),
            collection_name=self.cfg.COLLECTION_NAME,
        )
        self.generator = Generator()

    AREA_KEYWORDS = {
        "académic": "Dirección Académica",
        "academ": "Dirección Académica",
        "reglamento": "Dirección Académica",
        "estudiante": "Soporte al Estudiante",
        "beca": "Dirección Académica",
        "reembolso": "Dirección Académica",
        "rh": "Recursos Humanos",
        "recursos humanos": "Recursos Humanos",
        "inducción": "Recursos Humanos",
        "remoto": "Recursos Humanos",
        "vacaciones": "Recursos Humanos",
        "licencia": "Recursos Humanos",
        "nomina": "Recursos Humanos",
        "nómina": "Recursos Humanos",
        "contrato laboral": "Recursos Humanos",
        "jurídic": "Área Jurídica",
        "legal": "Área Jurídica",
        "abogad": "Área Jurídica",
        "privacidad": "Área Jurídica",
        "datos personales": "Área Jurídica",
        "terminos": "Área Jurídica",
        "términos": "Área Jurídica",
        "facturación": "Dirección Financiera",
        "facturacion": "Dirección Financiera",
        "presupuesto": "Dirección Financiera",
        "financier": "Dirección Financiera",
        "pago": "Dirección Financiera",
        "cobranza": "Dirección Financiera",
        "cartera": "Dirección Financiera",
        "soporte": "Coordinación de Soporte",
        "operaciones": "Coordinación de Soporte",
        "sla": "Coordinación de Soporte",
        "ticket": "Coordinación de Soporte",
        "continuidad": "Coordinación de Soporte",
        "comercial": "Dirección Comercial",
        "marketing": "Dirección Comercial",
        "precio": "Dirección Comercial",
        "catálogo": "Dirección Comercial",
        "catalogo": "Dirección Comercial",
        "ingeniería": "Equipo de Ingeniería",
        "ingenieria": "Equipo de Ingeniería",
        "devops": "Equipo de Ingeniería",
        "despliegue": "Equipo de Ingeniería",
        "arquitectura": "Equipo de Ingeniería",
        "producto": "Equipo de Producto",
        "calidad": "Coordinación de Calidad",
    }

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    QUERY_EXPANSIONS = {
        "estandar": " Guia de Estandares de Codigo Python TypeScript Java Ruff ESLint Git Flow code review coverage tests",
        "codigo": " Guia de Estandares de Codigo Python TypeScript Java Ruff ESLint Git Flow code review coverage tests",
        "programacion": " Guia de Estandares de Codigo Python TypeScript Java convenciones",
        "referido": " link unico credito descuento recomendar amigo familiar inscripcion Programa de Fidelizacion y Referidos",
        "fidelizacion": " Programa de Fidelizacion y Referidos niveles Bronce Plata Oro descuento puntos",
        "utilidad neta": " Estados Financieros 2025 Balance General P&L 560 millones 270 millones",
        "ganancia": " Estados Financieros 2025 Balance General P&L 560 millones",
        "financiero": " Estados Financieros 2025 presupuesto ingresos balance P&L",
        "balance": " Estados Financieros 2025 activo pasivo patrimonio balance general 2050 millones",
        "convenio corporativo": " Programa de Convenios Corporativos empresas descuentos volumen B2B empleados",
        "convenio": " Programa de Convenios Corporativos empresas descuentos volumen B2B",
    }

    def _expand_query(self, question: str) -> str:
        q = question.lower()
        for keyword, expansion in self.QUERY_EXPANSIONS.items():
            if keyword in q:
                log.info(f"Query expandida con '{keyword}'")
                return f"{question} {expansion}"
        return question

    def ask(self, question: str, top_k: int = 5) -> dict:
        log.info(f"Pregunta: {question}")

        expanded = self._expand_query(question)
        query_emb = self.embedder.embed([expanded])[0]
        results = self.indexer.search(query_emb, top_k=top_k)

        if not results:
            return self._fallback_con_contacto(question)

        best_dist = results[0]["distancia"]
        best_score = 1 - best_dist
        if best_score < self.cfg.CONFIDENCE_THRESHOLD:
            log.info(
                f"Confianza baja ({best_score:.3f} < {self.cfg.CONFIDENCE_THRESHOLD}) "
                "- activando fallback"
            )
            return self._fallback_con_contacto(question)

        context_parts, fuentes = self._armar_contexto(results)

        respuesta_raw = self.generator.generate(question, context_parts)

        es_valida = self.generator.verificar_alucinacion(
            respuesta_raw, context_parts
        )
        if not es_valida:
            log.warning("Posible alucinación detectada, usando fallback")
            return self._fallback_con_contacto(question)

        respuesta = self._formatear_respuesta(respuesta_raw, fuentes)
        return {
            "pregunta": question,
            "respuesta": respuesta,
            "fuentes": fuentes,
            "confianza": round(best_score, 4),
        }

    # ------------------------------------------------------------------
    # Construcción del contexto para el prompt
    # ------------------------------------------------------------------

    def _armar_contexto(
        self, results: list[dict]
    ) -> tuple[list[dict], list[dict]]:
        chunk_ids = [r["id"] for r in results]
        fetched = self.indexer.collection.get(
            ids=chunk_ids, include=["documents", "metadatas"]
        )

        chunk_map = {}
        if fetched and fetched.get("ids"):
            for i in range(len(fetched["ids"])):
                cid = fetched["ids"][i]
                chunk_map[cid] = {
                    "text": fetched["documents"][i],
                    "seccion": fetched["metadatas"][i].get("seccion", ""),
                }

        context_parts = []
        fuentes = []
        seen_titles = set()

        for r in results:
            title = r["documento"]
            chunk_data = chunk_map.get(r["id"], {})
            full_text = chunk_data.get("text", r["contenido"])
            seccion = chunk_data.get("seccion", "") or r.get("seccion", "")

            if title not in seen_titles:
                seen_titles.add(title)
                fuentes.append({
                    "titulo": title,
                    "categoria": r["categoria"],
                    "seccion": seccion,
                    "relevancia": round(1 - r["distancia"], 4),
                })

            context_parts.append({
                "titulo": title,
                "seccion": seccion,
                "texto": full_text,
            })

        return context_parts, fuentes

    # ------------------------------------------------------------------
    # Formateo de la respuesta final
    # ------------------------------------------------------------------

    def _formatear_respuesta(
        self, respuesta_raw: str, fuentes: list[dict]
    ) -> str:
        fuentes_lines = []
        for f in fuentes:
            label = f["titulo"]
            if f.get("seccion"):
                label += f" / {f['seccion']}"
            fuentes_lines.append(f"- {label}")

        return (
            f"{respuesta_raw}\n\n"
            "---\n"
            "Fuentes consultadas:\n" + "\n".join(fuentes_lines)
        )

    # ------------------------------------------------------------------
    # Fallback con contacto de área
    # ------------------------------------------------------------------

    def _fallback_con_contacto(self, question: str) -> dict:
        q = question.lower()
        area = None
        for keyword, nombre_area in self.AREA_KEYWORDS.items():
            if keyword in q:
                area = nombre_area
                break

        if area:
            contact_text = self._buscar_contacto_area(area)
            if contact_text:
                return {
                    "pregunta": question,
                    "respuesta": (
                        "No encontré información sobre esa pregunta en los documentos "
                        "disponibles de AprendeYa.\n\n"
                        "Puedes contactar al área responsable:\n\n"
                        f"{contact_text}\n\n"
                        "---\n"
                        "Fuente: Directorio de Contactos por Área (REF-001)."
                    ),
                    "fuentes": [{
                        "titulo": "Directorio de Contactos por Área",
                        "categoria": "REF",
                        "relevancia": 1.0,
                    }],
                }

        return {
            "pregunta": question,
            "respuesta": (
                "No encontré información relevante en los documentos disponibles "
                "de AprendeYa. Puedes consultar el Directorio de Contactos por Área "
                "(REF-001) en el sitio web de AprendeYa para comunicarte con el área "
                "que pueda ayudarte, o escribir a soporte@aprendeya.com."
            ),
            "fuentes": [],
        }

    def _buscar_contacto_area(self, area: str) -> str | None:
        query_emb = self.embedder.embed([f"contacto {area}"])[0]
        contact_results = self.indexer.search(query_emb, top_k=12)
        if not contact_results:
            return None
        cids = [r["id"] for r in contact_results]
        fetched = self.indexer.collection.get(
            ids=cids, include=["documents", "metadatas"]
        )
        if not fetched or not fetched.get("ids"):
            return None
        for i in range(len(fetched["ids"])):
            seccion = (fetched["metadatas"][i] or {}).get("seccion", "")
            if area.lower() in seccion.lower():
                return fetched["documents"][i][:600]
        return fetched["documents"][0][:600]
