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

    avaliacoes = relationship("Avaliacao", back_populates="usuario")

class Filme(Base):
    __tablename__ = 'filmes'
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    genero = Column(String, index=True)
    diretor = Column(String)
    atores = Column(String)

    avaliacoes = relationship("Avaliacao", back_populates="filme")

class Avaliacao(Base):
    __tablename__ = 'avaliacoes'
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    filme_id = Column(Integer, ForeignKey('filmes.id'))
    avaliacao = Column(Float, nullable=True)
    
    usuario = relationship("Usuario", back_populates="avaliacoes")
    filme = relationship("Filme", back_populates="avaliacoes")
