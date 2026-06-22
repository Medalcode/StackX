from sqlalchemy import Column, Float, ForeignKey, Index, Integer, String, Text
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
    category_id = Column(Integer, ForeignKey('categories.id'), index=True)

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
    tech_id = Column(Integer, ForeignKey('technologies.id'), nullable=False, index=True)
    attr_id = Column(Integer, ForeignKey('attributes.id'), nullable=False, index=True)
    value = Column(Float, nullable=False)

    technology = relationship('Technology', back_populates='scores')
    attribute = relationship('Attribute', back_populates='scores')

    __table_args__ = (
        Index('ix_techscores_tech_attr', 'tech_id', 'attr_id', unique=True),
    )


class Compatibility(Base):
    __tablename__ = 'compatibilities'
    id = Column(Integer, primary_key=True)
    tech_a = Column(Integer, ForeignKey('technologies.id'), nullable=False, index=True)
    tech_b = Column(Integer, ForeignKey('technologies.id'), nullable=False, index=True)
    score = Column(Float, nullable=False)
    reason = Column(Text, nullable=True)
