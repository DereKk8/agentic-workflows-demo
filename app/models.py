from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    curso: Mapped[str] = mapped_column(String(120), nullable=False)
    estado: Mapped[str] = mapped_column(String(60), default="abierto")
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class ArticuloConocimiento(Base):
    __tablename__ = "articulos_conocimiento"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    contenido: Mapped[str] = mapped_column(Text, nullable=False)
    categoria: Mapped[str] = mapped_column(String(120), nullable=False)
    etiquetas: Mapped[str] = mapped_column(String(250), default="")
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class EjecucionAgente(Base):
    __tablename__ = "ejecuciones_agente"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ticket_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    modo: Mapped[str] = mapped_column(String(20), nullable=False)
    proveedor: Mapped[str] = mapped_column(String(40), nullable=False)
    clasificacion: Mapped[str] = mapped_column(String(120), nullable=False)
    articulos_usados: Mapped[str] = mapped_column(Text, default="")
    respuesta_sugerida: Mapped[str] = mapped_column(Text, nullable=False)
    requiere_escalamiento: Mapped[bool] = mapped_column(Boolean, default=False)
    razon_escalamiento: Mapped[str] = mapped_column(Text, default="")
    pasos_json: Mapped[str] = mapped_column(Text, default="[]")
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

