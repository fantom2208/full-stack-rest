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
    name = Column(String(64), nullable=False)
    description = Column(String(256))
    address = Column(String(64), nullable=False)
    
    # We added this serialize function to be able to send JSON objects
    # in a serializable format
    @property
    def serialize(self):
        return {'id'             : self.id,
                'name'           : self.name,
                'description'    : self.description,
                'address'        : self.address}


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
    name = Column(String(64), nullable = False)
    description = Column(String(250))
    course = Column(String(16))
    weight = Column(Integer)
    content = Column(String(128))
    
    # We added this serialize function to be able to send JSON objects
    # in a serializable format
    @property
    def serialize(self):
        return {'id'             : self.id,
                'name'           : self.name,
                'description'    : self.description,
                'course'         : self.course,
                'weight'         : self.weight,
                'content'        : self.content}

## class RestaurantMenuItem 
class RestMenuItem(Base):
    ## variable to refer to 'rest_menu_item' table
    __tablename__ = 'rest_menu_item'

    id = Column(Integer, primary_key = True)
    ### restaurant_id - foreign key
    ### values to take from table 'restaurant' column 'id'
    restaurant_id = Column(Integer,ForeignKey('restaurant.id'))
    ### tell SQLAlchemy relationship one table (class) to another 
    restaurant = relationship(Restaurant) 

    ### menu_id - foreign key
    ### values to take from table 'menu_item' column 'id'
    menu_item_id = Column(Integer,ForeignKey('menu_item.id'))
    ### tell SQLAlchemy relationship one table (class) to another 
    menu_item = relationship(MenuItem) 

    ### why price is a string? not integer?
    price = Column(Integer, nullable=False)
    comment = Column(String(128))

    # We added this serialize function to be able to send JSON objects
    # in a serializable format
    @property
    def serialize(self):
        return {'id'             : self.id,
                'restaurant_id'  : self.restaurant_id,
                'menu_item_id'   : self.menu_item_id,
                'price'          : self.price,
                'comment'        : self.comment}
# end of CONFIGURATION

def create_db():
    # instance (example) of engine class and point (connect) to database we used 
    # first engine will create database in SQLite 3
    engine = create_engine('sqlite:///restaurantmenu.db')    
    # goes into DB and adds classes as new tables in our DB 
    Base.metadata.create_all(engine)

    return 'Database was created!'


# if mani module to execute
if __name__ == '__main__':
    # create databse
    print(create_db())