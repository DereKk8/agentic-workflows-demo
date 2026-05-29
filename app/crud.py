import json

from sqlalchemy.orm import Session

from app import models, schemas


def listar_tickets(db: Session):
    return db.query(models.Ticket).order_by(models.Ticket.id.desc()).all()


def crear_ticket(db: Session, data: schemas.TicketCreate):
    item = models.Ticket(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def obtener_ticket(db: Session, ticket_id: int):
    return db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()


def actualizar_ticket(db: Session, ticket_id: int, data: schemas.TicketUpdate):
    item = obtener_ticket(db, ticket_id)
    if not item:
        return None
    for key, value in data.model_dump().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


def eliminar_ticket(db: Session, ticket_id: int):
    item = obtener_ticket(db, ticket_id)
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True


def listar_articulos(db: Session):
    return db.query(models.ArticuloConocimiento).order_by(models.ArticuloConocimiento.id.desc()).all()


def crear_articulo(db: Session, data: schemas.ArticuloCreate):
    item = models.ArticuloConocimiento(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def obtener_articulo(db: Session, articulo_id: int):
    return db.query(models.ArticuloConocimiento).filter(models.ArticuloConocimiento.id == articulo_id).first()


def actualizar_articulo(db: Session, articulo_id: int, data: schemas.ArticuloUpdate):
    item = obtener_articulo(db, articulo_id)
    if not item:
        return None
    for key, value in data.model_dump().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


def eliminar_articulo(db: Session, articulo_id: int):
    item = obtener_articulo(db, articulo_id)
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True


def crear_ejecucion(
    db: Session,
    ticket_id: int,
    modo: str,
    proveedor: str,
    clasificacion: str,
    articulos_usados: list[int],
    respuesta_sugerida: str,
    requiere_escalamiento: bool,
    razon_escalamiento: str,
    pasos: list[dict],
):
    item = models.EjecucionAgente(
        ticket_id=ticket_id,
        modo=modo,
        proveedor=proveedor,
        clasificacion=clasificacion,
        articulos_usados=json.dumps(articulos_usados),
        respuesta_sugerida=respuesta_sugerida,
        requiere_escalamiento=requiere_escalamiento,
        razon_escalamiento=razon_escalamiento,
        pasos_json=json.dumps(pasos, ensure_ascii=False),
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def listar_ejecuciones_por_ticket(db: Session, ticket_id: int):
    return (
        db.query(models.EjecucionAgente)
        .filter(models.EjecucionAgente.ticket_id == ticket_id)
        .order_by(models.EjecucionAgente.id.desc())
        .all()
    )

