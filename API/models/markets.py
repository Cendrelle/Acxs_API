from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Configuration de SQLAlchemy
Base = declarative_base()

class PlanDePassation(Base):
    __tablename__ = 'plans_de_passation'
    id = Column(Integer, primary_key=True, autoincrement=True)
    plan_id = Column(String, unique=True, nullable=False)
    nom_autorite_contractante = Column(String, nullable=False)
    periode_couverte = Column(String, nullable=False)
    marches = relationship("Marche", back_populates="plan")

class Marche(Base):
    __tablename__ = 'marches'
    id = Column(Integer, primary_key=True, autoincrement=True)
    plan_id = Column(String, ForeignKey('plans_de_passation.plan_id'), nullable=False)
    n = Column(Integer)  # Numéro du marché
    reference = Column(String)
    description = Column(String, nullable=False)
    type_marche = Column(String)
    montant_fcfa = Column(Float)
    date_approbation_marche = Column(Date)
    statut = Column(String)  # "passé" ou "à venir"
    plan = relationship("PlanDePassation", back_populates="marches")

# Connexion à la base de données SQLite
engine = create_engine('sqlite:///marches.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()