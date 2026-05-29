from datetime import datetime

from pydantic import BaseModel


class TicketBase(BaseModel):
    titulo: str
    descripcion: str
    curso: str
    estado: str = "abierto"


class TicketCreate(TicketBase):
    pass


class TicketUpdate(TicketBase):
    pass


class TicketOut(TicketBase):
    id: int
    creado_en: datetime
    actualizado_en: datetime

    class Config:
        from_attributes = True


class ArticuloBase(BaseModel):
    titulo: str
    contenido: str
    categoria: str
    etiquetas: str = ""


class ArticuloCreate(ArticuloBase):
    pass


class ArticuloUpdate(ArticuloBase):
    pass


class ArticuloOut(ArticuloBase):
    id: int
    creado_en: datetime
    actualizado_en: datetime

    class Config:
        from_attributes = True


class PasoWorkflow(BaseModel):
    nombre: str
    estado: str
    detalle: str


class EjecutarWorkflowOut(BaseModel):
    ejecucion_id: int
    ticket_id: int
    clasificacion: str
    articulos_usados: list[int]
    respuesta_sugerida: str
    requiere_escalamiento: bool
    razon_escalamiento: str
    pasos: list[PasoWorkflow]
    modo: str
    proveedor: str


class EjecucionOut(BaseModel):
    id: int
    ticket_id: int
    modo: str
    proveedor: str
    clasificacion: str
    articulos_usados: list[int]
    respuesta_sugerida: str
    requiere_escalamiento: bool
    razon_escalamiento: str
    pasos: list[PasoWorkflow]
    creado_en: datetime

