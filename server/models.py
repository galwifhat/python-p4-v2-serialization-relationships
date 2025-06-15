# server/models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Zookeeper(db.Model, SerializerMixin):
    __tablename__ = "zookeepers"

    # serialize_only = (
    #     "id",
    #     "name",
    #     "animals.name",
    #     "animals.species",
    # )
    # serialize_rules = ()

    serialize_rules = ("-animals.zookeeper",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    birthday = db.Column(db.Date)

    animals = db.relationship("Animal", back_populates="zookeeper")

    # enforce a specific key order
    def to_dict(self, *args, **kwargs):
        data = super().to_dict(*args, **kwargs)
        return {"id": data["id"], "name": data["name"], "birthday": data["birthday"]}


class Enclosure(db.Model, SerializerMixin):
    __tablename__ = "enclosures"

    # serilization rules
    serialize_rules = ("-animals.enclosure",)

    id = db.Column(db.Integer, primary_key=True)
    environment = db.Column(db.String)
    open_to_visitors = db.Column(db.Boolean)

    animals = db.relationship("Animal", back_populates="enclosure")


class Animal(db.Model, SerializerMixin):
    __tablename__ = "animals"

    serialize_rules = (
        "-zookeeper.animals",
        "-enclosure.animals",
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    species = db.Column(db.String)

    zookeeper_id = db.Column(db.Integer, db.ForeignKey("zookeepers.id"))
    enclosure_id = db.Column(db.Integer, db.ForeignKey("enclosures.id"))

    enclosure = db.relationship("Enclosure", back_populates="animals")
    zookeeper = db.relationship("Zookeeper", back_populates="animals")

    def __repr__(self):
        return f"<Animal {self.name}, a {self.species}>"
