import json
import re
from dataclasses import dataclass

from crewai import Agent, Crew, LLM, Task
from sqlalchemy.orm import Session

from app import models
from app.settings import settings


@dataclass
class ResultadoWorkflow:
    clasificacion: str
    articulos_usados: list[int]
    respuesta_sugerida: str
    requiere_escalamiento: bool
    razon_escalamiento: str
    pasos: list[dict]
    modo: str
    proveedor: str


def _clasificar_ticket(ticket: models.Ticket) -> str:
    texto = f"{ticket.titulo} {ticket.descripcion}".lower()
    if any(x in texto for x in ["matrícula", "inscripción", "registro"]):
        return "administrativo"
    if any(x in texto for x in ["nota", "calificación", "evaluación", "examen"]):
        return "académico"
    if any(x in texto for x in ["plataforma", "error", "acceso", "sistema"]):
        return "técnico"
    return "general"


def _buscar_articulos(db: Session, ticket: models.Ticket, clasificacion: str) -> list[models.ArticuloConocimiento]:
    terms = set((f"{ticket.titulo} {ticket.descripcion} {clasificacion}").lower().split())
    candidatos = db.query(models.ArticuloConocimiento).all()

    scored = []
    for art in candidatos:
        texto = f"{art.titulo} {art.contenido} {art.categoria} {art.etiquetas}".lower()
        score = sum(1 for t in terms if t in texto)
        scored.append((score, art))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [art for score, art in scored if score > 0][:3]


def _respuesta_mock(ticket: models.Ticket, clasificacion: str, articulos: list[models.ArticuloConocimiento]) -> str:
    titulos = ", ".join([a.titulo for a in articulos]) if articulos else "sin artículos relacionados"
    return (
        f"Hola. Hemos analizado tu solicitud '{ticket.titulo}' del curso {ticket.curso}. "
        f"Se clasificó como caso {clasificacion}. "
        f"Con base en {titulos}, te sugerimos seguir las instrucciones institucionales correspondientes "
        "y responder a este ticket si necesitas más apoyo."
    )


def _supervisar_mock(ticket: models.Ticket, clasificacion: str) -> tuple[bool, str]:
    texto = f"{ticket.titulo} {ticket.descripcion}".lower()
    if clasificacion == "académico" and any(x in texto for x in ["injusta", "apelación", "apelacion"]):
        return True, "Requiere revisión de coordinación académica por posible apelación."
    if clasificacion == "técnico" and any(x in texto for x in ["no funciona", "caído", "caido"]):
        return True, "Requiere revisión del equipo de TI por posible incidencia crítica."
    return False, "No se requiere escalamiento en esta ejecución."


def _build_llm():
    proveedor = settings.proveedor_llm.lower()
    if proveedor == "groq":
        if not settings.groq_api_key:
            raise RuntimeError("Falta GROQ_API_KEY para modo real.")
        from langchain_groq import ChatGroq

        return ChatGroq(api_key=settings.groq_api_key, model=settings.model_groq)
    if proveedor == "openrouter":
        if not settings.openrouter_api_key:
            raise RuntimeError("Falta OPENROUTER_API_KEY para modo real.")
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            api_key=settings.openrouter_api_key,
            model=settings.model_openrouter,
            base_url="https://openrouter.ai/api/v1",
        )
    if proveedor == "gemini":
        if not settings.gemini_api_key:
            raise RuntimeError("Falta GEMINI_API_KEY para modo real.")
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(api_key=settings.gemini_api_key, model=settings.model_gemini)
    raise RuntimeError(f"Proveedor no soportado: {proveedor}")


def _build_crewai_llm() -> LLM:
    proveedor = settings.proveedor_llm.lower()
    if proveedor == "groq":
        if not settings.groq_api_key:
            raise RuntimeError("Falta GROQ_API_KEY para modo real.")
        return LLM(model=f"groq/{settings.model_groq}", api_key=settings.groq_api_key)
    if proveedor == "openrouter":
        if not settings.openrouter_api_key:
            raise RuntimeError("Falta OPENROUTER_API_KEY para modo real.")
        return LLM(
            model=settings.model_openrouter,
            api_key=settings.openrouter_api_key,
            base_url="https://openrouter.ai/api/v1",
        )
    if proveedor == "gemini":
        if not settings.gemini_api_key:
            raise RuntimeError("Falta GEMINI_API_KEY para modo real.")
        model = settings.model_gemini if "/" in settings.model_gemini else f"gemini/{settings.model_gemini}"
        return LLM(model=model, api_key=settings.gemini_api_key)
    raise RuntimeError(f"Proveedor no soportado: {proveedor}")


def _parse_supervision_json(raw: str) -> dict | None:
    texto = (raw or "").strip()
    if not texto:
        return None
    try:
        data = json.loads(texto)
        if isinstance(data, dict):
            return data
    except Exception:
        pass

    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", texto, flags=re.DOTALL | re.IGNORECASE)
    if fenced:
        try:
            data = json.loads(fenced.group(1))
            if isinstance(data, dict):
                return data
        except Exception:
            pass

    inline = re.search(r"(\{.*\})", texto, flags=re.DOTALL)
    if inline:
        try:
            data = json.loads(inline.group(1))
            if isinstance(data, dict):
                return data
        except Exception:
            return None
    return None


def _respuesta_supervision_real(ticket: models.Ticket, clasificacion: str, articulos: list[models.ArticuloConocimiento]):
    llm = _build_llm()
    crew_llm = _build_crewai_llm()
    contexto = "\n".join([f"- {a.titulo}: {a.contenido[:220]}" for a in articulos]) or "- Sin artículos"

    # Fuerza el proveedor configurado y evita fallback implícito a LiteLLM/OpenAI.
    redactor = Agent(
        role="Redactor",
        goal="Redactar respuesta útil y clara",
        backstory="Asistente académico",
        llm=crew_llm,
    )
    supervisor = Agent(
        role="Supervisor",
        goal="Evaluar riesgo y escalamiento",
        backstory="Coordinador académico",
        llm=crew_llm,
    )

    task_respuesta = Task(
        description=(
            "Escribe una respuesta corta en español para el ticket.\n"
            f"TICKET: {ticket.titulo}\nDETALLE: {ticket.descripcion}\nCURSO: {ticket.curso}\n"
            f"CLASIFICACION: {clasificacion}\nCONOCIMIENTO:\n{contexto}\n"
            "Devuelve solo la respuesta final."
        ),
        expected_output="Respuesta final en español",
        agent=redactor,
    )
    task_supervision = Task(
        description=(
            "Determina si se debe escalar. Devuelve JSON con llaves: "
            "requiere_escalamiento (boolean) y razon_escalamiento (string).\n"
            f"TICKET: {ticket.titulo}\nDETALLE: {ticket.descripcion}\nCLASIFICACION: {clasificacion}"
        ),
        expected_output="JSON válido con decisión de escalamiento",
        agent=supervisor,
    )

    crew = Crew(agents=[redactor, supervisor], tasks=[task_respuesta, task_supervision], llm=crew_llm, verbose=False)
    _ = crew.kickoff()

    resp_prompt = task_respuesta.description
    sup_prompt = task_supervision.description
    respuesta = llm.invoke(resp_prompt).content
    supervision = llm.invoke(sup_prompt).content
    parsed = _parse_supervision_json(supervision)
    if parsed is None:
        reparacion_prompt = (
            "Convierte el siguiente contenido a JSON estricto y devuelve SOLO el JSON con llaves "
            "`requiere_escalamiento` (boolean) y `razon_escalamiento` (string), sin texto adicional:\n\n"
            f"{supervision}"
        )
        reparada = llm.invoke(reparacion_prompt).content
        parsed = _parse_supervision_json(reparada)

    if parsed is None:
        esc = False
        razon = "La supervisión real no devolvió JSON válido; se mantiene no escalado."
    else:
        esc = bool(parsed.get("requiere_escalamiento", False))
        razon = str(parsed.get("razon_escalamiento", "Sin razón."))
    return respuesta.strip(), esc, razon


def ejecutar_workflow(db: Session, ticket: models.Ticket) -> ResultadoWorkflow:
    pasos = []
    clasificacion = _clasificar_ticket(ticket)
    pasos.append({"nombre": "Clasificador", "estado": "ok", "detalle": f"Ticket clasificado como {clasificacion}."})

    articulos = _buscar_articulos(db, ticket, clasificacion)
    ids = [a.id for a in articulos]
    pasos.append({"nombre": "Buscador de conocimiento", "estado": "ok", "detalle": f"Se encontraron {len(ids)} artículos relevantes."})

    modo = settings.modo_agente.lower()
    proveedor = settings.proveedor_llm.lower()
    if modo == "real":
        try:
            respuesta, escalar, razon = _respuesta_supervision_real(ticket, clasificacion, articulos)
            pasos.append({"nombre": "Redactor", "estado": "ok", "detalle": "Respuesta redactada con LLM."})
            pasos.append({"nombre": "Supervisor", "estado": "ok", "detalle": "Supervisión completada con LLM."})
        except Exception as exc:
            respuesta = _respuesta_mock(ticket, clasificacion, articulos)
            escalar, razon = _supervisar_mock(ticket, clasificacion)
            pasos.append({"nombre": "Redactor", "estado": "fallback", "detalle": "Fallo en modo real; se aplicó respuesta mock."})
            pasos.append({"nombre": "Supervisor", "estado": "fallback", "detalle": f"Fallo en modo real: {exc}"})
    else:
        respuesta = _respuesta_mock(ticket, clasificacion, articulos)
        escalar, razon = _supervisar_mock(ticket, clasificacion)
        pasos.append({"nombre": "Redactor", "estado": "ok", "detalle": "Respuesta generada con plantilla determinista."})
        pasos.append({"nombre": "Supervisor", "estado": "ok", "detalle": "Supervisión determinista completada."})

    return ResultadoWorkflow(
        clasificacion=clasificacion,
        articulos_usados=ids,
        respuesta_sugerida=respuesta,
        requiere_escalamiento=escalar,
        razon_escalamiento=razon,
        pasos=pasos,
        modo=modo,
        proveedor=proveedor,
    )

