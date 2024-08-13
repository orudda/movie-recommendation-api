from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)

    historico = relationship("Historico", back_populates="usuario")

class Filme(Base):
    __tablename__ = 'filmes'
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    genero = Column(String, index=True)
    diretor = Column(String)
    ano = Column(Integer)

    historico = relationship("Historico", back_populates="filme")

class Historico(Base):
    __tablename__ = 'historico'
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    filme_id = Column(Integer, ForeignKey('filmes.id'))
    data_visualizacao = Column(DateTime, default=datetime.utcnow)
    avaliacao = Column(Float, nullable=True)
    
    usuario = relationship("Usuario", back_populates="historico")
    filme = relationship("Filme", back_populates="historico")
