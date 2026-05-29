import json
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app import crud, models, schemas, workflow
from app.db import Base, engine, get_db
from app.settings import settings

app = FastAPI(title=settings.app_name)
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


def seed_data(db: Session):
    if db.query(models.Ticket).count() == 0:
        db.add_all(
            [
                models.Ticket(
                    titulo="Problema con calificación final",
                    descripcion="Considero que mi nota final no coincide con la rúbrica.",
                    curso="Arquitectura de Software",
                    estado="abierto",
                ),
                models.Ticket(
                    titulo="Error de acceso a la plataforma virtual",
                    descripcion="No puedo ingresar al aula virtual desde ayer.",
                    curso="Bases de Datos",
                    estado="abierto",
                ),
            ]
        )
    if db.query(models.ArticuloConocimiento).count() == 0:
        db.add_all(
            [
                models.ArticuloConocimiento(
                    titulo="Proceso de apelación de calificaciones",
                    contenido="El estudiante debe enviar solicitud formal en un plazo de 5 días hábiles.",
                    categoria="académico",
                    etiquetas="nota,apelación,evaluación",
                ),
                models.ArticuloConocimiento(
                    titulo="Guía de recuperación de acceso al campus virtual",
                    contenido="Verifique credenciales, restablezca contraseña y reporte fallas persistentes.",
                    categoria="técnico",
                    etiquetas="acceso,plataforma,soporte",
                ),
            ]
        )
    db.commit()


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    seed_data(db)
    db.close()


@app.get("/")
def home():
    return FileResponse(static_dir / "index.html")


@app.get("/api/health")
def health():
    return {"status": "ok", "app": settings.app_name}


@app.post("/api/seed")
def seed(db: Session = Depends(get_db)):
    seed_data(db)
    return {"mensaje": "Datos de demostración disponibles."}


@app.get("/api/tickets", response_model=list[schemas.TicketOut])
def get_tickets(db: Session = Depends(get_db)):
    return crud.listar_tickets(db)


@app.post("/api/tickets", response_model=schemas.TicketOut)
def post_ticket(data: schemas.TicketCreate, db: Session = Depends(get_db)):
    return crud.crear_ticket(db, data)


@app.put("/api/tickets/{ticket_id}", response_model=schemas.TicketOut)
def put_ticket(ticket_id: int, data: schemas.TicketUpdate, db: Session = Depends(get_db)):
    item = crud.actualizar_ticket(db, ticket_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return item


@app.delete("/api/tickets/{ticket_id}")
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ok = crud.eliminar_ticket(db, ticket_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return {"mensaje": "Ticket eliminado"}


@app.get("/api/articulos", response_model=list[schemas.ArticuloOut])
def get_articulos(db: Session = Depends(get_db)):
    return crud.listar_articulos(db)


@app.post("/api/articulos", response_model=schemas.ArticuloOut)
def post_articulo(data: schemas.ArticuloCreate, db: Session = Depends(get_db)):
    return crud.crear_articulo(db, data)


@app.put("/api/articulos/{articulo_id}", response_model=schemas.ArticuloOut)
def put_articulo(articulo_id: int, data: schemas.ArticuloUpdate, db: Session = Depends(get_db)):
    item = crud.actualizar_articulo(db, articulo_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    return item


@app.delete("/api/articulos/{articulo_id}")
def delete_articulo(articulo_id: int, db: Session = Depends(get_db)):
    ok = crud.eliminar_articulo(db, articulo_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    return {"mensaje": "Artículo eliminado"}


@app.post("/api/workflow/ejecutar/{ticket_id}", response_model=schemas.EjecutarWorkflowOut)
def ejecutar(ticket_id: int, db: Session = Depends(get_db)):
    ticket = crud.obtener_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    result = workflow.ejecutar_workflow(db, ticket)
    ejec = crud.crear_ejecucion(
        db=db,
        ticket_id=ticket_id,
        modo=result.modo,
        proveedor=result.proveedor,
        clasificacion=result.clasificacion,
        articulos_usados=result.articulos_usados,
        respuesta_sugerida=result.respuesta_sugerida,
        requiere_escalamiento=result.requiere_escalamiento,
        razon_escalamiento=result.razon_escalamiento,
        pasos=result.pasos,
    )
    return schemas.EjecutarWorkflowOut(
        ejecucion_id=ejec.id,
        ticket_id=ticket_id,
        clasificacion=result.clasificacion,
        articulos_usados=result.articulos_usados,
        respuesta_sugerida=result.respuesta_sugerida,
        requiere_escalamiento=result.requiere_escalamiento,
        razon_escalamiento=result.razon_escalamiento,
        pasos=[schemas.PasoWorkflow(**p) for p in result.pasos],
        modo=result.modo,
        proveedor=result.proveedor,
    )


@app.get("/api/tickets/{ticket_id}/ejecuciones", response_model=list[schemas.EjecucionOut])
def get_ejecuciones(ticket_id: int, db: Session = Depends(get_db)):
    items = crud.listar_ejecuciones_por_ticket(db, ticket_id)
    output = []
    for x in items:
        output.append(
            schemas.EjecucionOut(
                id=x.id,
                ticket_id=x.ticket_id,
                modo=x.modo,
                proveedor=x.proveedor,
                clasificacion=x.clasificacion,
                articulos_usados=json.loads(x.articulos_usados or "[]"),
                respuesta_sugerida=x.respuesta_sugerida,
                requiere_escalamiento=x.requiere_escalamiento,
                razon_escalamiento=x.razon_escalamiento,
                pasos=[schemas.PasoWorkflow(**p) for p in json.loads(x.pasos_json or "[]")],
                creado_en=x.creado_en,
            )
        )
    return output

