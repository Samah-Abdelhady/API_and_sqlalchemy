from database import db
import json
from sqlalchemy.dialects.postgresql import JSON
from collections import OrderedDict


class Unit_Data(db.Model):  
  __tablename__ = 'unit_data'

  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(), nullable=False)
  description = db.Column(db.String())
  expansion = db.Column(db.String(), nullable=False)
  age = db.Column(db.String(), nullable=False)
  created_in = db.Column(db.String(), nullable=False)
  cost = db.Column(JSON)##
  build_time = db.Column(db.Integer())
  reload_time = db.Column(db.Float())
  attack_delay = db.Column(db.Float())
  movement_rate = db.Column(db.Float())##
  line_of_sight = db.Column(db.Integer(), nullable=False)
  hit_points = db.Column(db.Integer(), nullable=False)
  range = db.Column(db.String())
  attack = db.Column(db.Integer())
  armor = db.Column(db.String(), nullable=False)
  attack_bonus = db.Column(db.String())
  armor_bonus = db.Column(db.String())
  search_radius = db.Column(db.Integer())
  accuracy = db.Column(db.String())
  blast_radius = db.Column(db.Float())

  
# sqlalchemy already did an init method for class attributes, so we don't have to creat init method


  def insert(self):
    db.session.add(self)
    db.session.commit()

  def format(self):
    data = [(
      'id', self.id),
    ('name', self.name),
    ('description', self.description),
    ('expansion', self.expansion),
    ('age', self.age),
    ('created_in', self.created_in),
    ('cost', self.cost),
    ('build_time', self.build_time),
    ('reload_time', self.reload_time),
    ('attack_delay', self.attack_delay),
    ('movement_rate', self.movement_rate),
    ('line_of_sight', self.line_of_sight),
    ('hit_points', self.hit_points),
    ('range', self.range),
    ('attack', self.attack),
    ('armor', self.armor),
    ('attack_bonus', self.attack_bonus.replace('[','').replace(']','').replace("'",'').split(",") if self.attack_bonus else None),
    ('armor_bonus', self.armor_bonus.replace('[','').replace(']','').replace("'",'').split(",") if self.armor_bonus else None),
    ('search_radius', self.search_radius),
    ('accuracy', self.accuracy),
    ('blast_radius', self.blast_radius)]

    final_data = OrderedDict([(key, value) for key, value in data if value])
    return final_data
    
 