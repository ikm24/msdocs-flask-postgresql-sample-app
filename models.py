from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import validates

from app import db


class ImagenCloud(db.Model):
    __tablename__ = 'imagen_cloud'
    id = Column(Integer, primary_key=True)
    usuario = Column(String(50))
    imagen = Column(String(50))
    tipo = Column(String(50))
    pixelesR = Column(Integer)
    pixelesG = Column(Integer)
    pixelesB = Column(Integer)
    fecha = Column(DateTime)

    def __str__(self):
        return self.name
