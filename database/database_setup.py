# database SQLAlchemy handling module 

# begin of CONFIGURATION
# rovides variables and functions to work with files
import os
# provides environment variables and functions
import sys
# classes to be used in MAPPER to connect python to DB 
from sqlalchemy import Column, ForeignKey, Integer, String
# class will be used in CONFIGURATION ans CLASS part 
from sqlalchemy.ext.declarative import declarative_base
# will be used to create foreign key relationsheep in MAPPER
from sqlalchemy.orm import relationship
# will be used in CONFIGURATION at the end of file
from sqlalchemy import create_engine
# will help to set up CLASS code (short name)
Base = declarative_base()


## CLASS part
### MAPPER part
## classes corresponds to specific tables in DB
## class Restaurant 
class Restaurant(Base):
    ## variable to refer to 'restaurant' table
    __tablename__ = 'restaurant'
   
    ### variables to connect to columns in DB
    ### also pass an attributes of columns
     ### id - primary key   
    id = Column(Integer, primary_key=True)
    ### nullable = False - column must have a value
    ### in order new row to be added
    name = Column(String(250), nullable=False)

## class MenuItem 
class MenuItem(Base):
    ## variable to refer to 'menu_item' table
    __tablename__ = 'menu_item'

    ### variables to connect to columns in DB
    ### also pass an attributes of columns
    ### id - primary key
    id = Column(Integer, primary_key = True)
    ### nullable = False - column must have a value
    ### in order new row to be added
    name =Column(String(80), nullable = False)
    description = Column(String(250))
    ### why price is a string? not integer?
    price = Column(String(8))
    course = Column(String(250))
    ### restaurant_id - foreign key
    ### values to take from table 'restaurant' column 'id'
    restaurant_id = Column(Integer,ForeignKey('restaurant.id'))
    ### tell SQLAlchemy relationship one table (class) to another 
    restaurant = relationship(Restaurant) 

#We added this serialize function to be able to send JSON objects in a serializable format
    @property
    def serialize(self):
       
       return {
           'name'           : self.name,
           'description'    : self.description,
           'id'             : self.id,
           'price'          : self.price,
           'course'         : self.course,
       }
 

# end of CONFIGURATION
# instance (example) of engine class and point (connect) 
# to database we used 
# first engine will create database in SQLite 3
engine = create_engine('sqlite:///restaurantmenu.db')
# goes into DB and adds classes as new tables in our DB 
Base.metadata.create_all(engine)