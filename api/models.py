import os
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy.dialects.postgresql import JSON


database_name = "age_of_empiress"
database_path = 'postgres://{}:{}@{}/{}'.format('postgres','postgres', 'localhost:5432', database_name)

db = SQLAlchemy()


# table to hold all units bounses from attack
class AttackBouns(db.Model):
  __tablename__ = 'attack_bouns'
  id = db.Column(db.Integer(), primary_key=True)
  attackBouns = db.Column(db.String())

  def insert(self):
    db.session.add(self)
    db.session.commit()


#table to compine between unit and unit_attack_bouns tables with many2many relationship
unit_attack_bouns = db.Table('unit_attack_bouns',
    db.Column('attack_bouns_id', db.Integer(), db.ForeignKey('attack_bouns.id'), primary_key=True),
    db.Column('unit_id', db.Integer(), db.ForeignKey('unit.id'), primary_key=True)
)



# table to hold all units bounses from armor
class ArmorBouns(db.Model):
  __tablename__ = 'armor_bouns'
  id = db.Column(db.Integer(), primary_key=True)
  armorBouns = db.Column(db.String())

  def insert(self):
    db.session.add(self)
    db.session.commit()


#table to compine between unit and unit_armor_bouns tables with many2many relationship
unit_armor_bouns = db.Table('unit_armor_bouns',
    db.Column('armor_bouns_id', db.Integer(), db.ForeignKey('armor_bouns.id'), primary_key=True),
    db.Column('unit_id', db.Integer(), db.ForeignKey('unit.id'), primary_key=True)
)




#Age of Empires units table
class Unit(db.Model):  
  __tablename__ = 'unit'

  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(), nullable=False)
  description = db.Column(db.String())
  expansion = db.Column(db.String(), nullable=False)
  age  = db.Column(db.String(), nullable=False)
  created_in = db.Column(db.String(), nullable=False)
  # wood, food, stone, gold ==> will be read as cost
  cost = db.Column(JSON, nullable=False)
  # wood_cost = db.Column(db.Integer(), nullable=False)
  # food_cost = db.Column(db.Integer(), nullable=False)
  # stone_cost = db.Column(db.Integer(), nullable=False)
  # gold_cost = db.Column(db.Integer(0, nullable=False))

  build_time = db.Column(db.Integer(), nullable=False)
  reload_time = db.Column(db.Numeric(), nullable=False)#Float()
  attack_delay = db.Column(db.Numeric())
  movement_rate = db.Column(db.Numeric(), nullable=False)
  line_of_sight = db.Column(db.Integer(), nullable=False)
  hit_points = db.Column(db.Integer(), nullable=False)
  unit_range = db.Column(db.String())
  attack = db.Column(db.Integer(), nullable=False)
  armor = db.Column(db.String(), nullable=False)
  search_radius = db.Column(db.Integer())
  accuracy = db.Column(db.String())
  blast_radius = db.Column(db.Numeric())

  attack_bonuses = db.relationship('AttackBouns',
      secondary=unit_attack_bouns,
      backref=db.backref('units',
      lazy=True))

  armor_bonuses = db.relationship('ArmorBouns',
      secondary=unit_armor_bouns,
      backref=db.backref('units',
      lazy=True))

# sqlalchemy already did an init method for class attributes, so we don't have to creat init method


  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  