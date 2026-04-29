from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)

    technologies = relationship('Technology', back_populates='category')

class Technology(Base):
    __tablename__ = 'technologies'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey('categories.id'))

    category = relationship('Category', back_populates='technologies')
    scores = relationship('TechScore', back_populates='technology')

class Attribute(Base):
    __tablename__ = 'attributes'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    unit = Column(String, nullable=True)

    scores = relationship('TechScore', back_populates='attribute')

class TechScore(Base):
    __tablename__ = 'tech_scores'
    id = Column(Integer, primary_key=True)
    tech_id = Column(Integer, ForeignKey('technologies.id'), nullable=False)
    attr_id = Column(Integer, ForeignKey('attributes.id'), nullable=False)
    value = Column(Float, nullable=False)

    technology = relationship('Technology', back_populates='scores')
    attribute = relationship('Attribute', back_populates='scores')

class Compatibility(Base):
    __tablename__ = 'compatibilities'
    id = Column(Integer, primary_key=True)
    tech_a = Column(Integer, ForeignKey('technologies.id'), nullable=False)
    tech_b = Column(Integer, ForeignKey('technologies.id'), nullable=False)
    score = Column(Float, nullable=False)
    reason = Column(Text, nullable=True)
