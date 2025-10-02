from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Recipe(Base):
    __tablename__ = 'recipes'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    cuisine = Column(String(100))
    category = Column(String(100))
    instructions = Column(Text)
    image_url = Column(String(500))
    
    ingredients = relationship('Ingredient', back_populates='recipe', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Recipe {self.name}>'

class Ingredient(Base):
    __tablename__ = 'ingredients'
    
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable=False)
    name = Column(String(200), nullable=False)
    measure = Column(String(100))
    
    recipe = relationship('Recipe', back_populates='ingredients')
    
    def __repr__(self):
        return f'<Ingredient {self.name}>'

engine = create_engine('sqlite:///globalkitchen.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
