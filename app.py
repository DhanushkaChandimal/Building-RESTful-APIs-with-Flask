# python -m venv venv
# venv\Scripts\Activate
# pip install Flask Flask-SQLAlchemy Flask-Marshmallow mysql-connector-python marshmallow-sqlalchemy
# CREATE DATABASE flask_api_db;

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, Table, Column, String, Integer
from marshmallow import ValidationError
from typing import List, Optional

# Initialize Flask app
app = Flask(__name__)

# MySQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost/flask_api_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creating our Base Model
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy and Marshmallow
db = SQLAlchemy(model_class=Base)
db.init_app(app)
ma = Marshmallow(app)

# Association Table
user_pet = Table(
    "user_pet",
    Base.metadata,
    Column("user_id", ForeignKey("user_account.id"), primary_key=True),
    Column("pet_id", ForeignKey("pets.id"), primary_key=True)
)

# Models
class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(200))
    
    #One-to-Many relationship from this User to a List of Pet Objects
    pets: Mapped[List["Pet"]] = relationship("Pet", secondary=user_pet, back_populates="owners")

class Pet(Base):
    __tablename__ = "pets"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    animal: Mapped[str] = mapped_column(String(200), nullable=False)
    
    # One-to-Many relationship, One pet can be related to a List of Users
    owners: Mapped[List["User"]] = relationship("User", secondary=user_pet, back_populates="pets")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)