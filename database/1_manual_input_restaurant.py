# inserting data to table restaurant module

# Connection to DB and adding information in tables via script
# create_engine will point (connect) to database we used 
from sqlalchemy import create_engine
# import to make connection to 
from sqlalchemy.orm import sessionmaker
# from initial setup module import CLASSES 
from database_setup import Base, MenuItem, Restaurant


def set_connection():
    # set connection to db (from end of CONFIGURATION)
    # instance (example) of engine class and connect to database 
    engine = create_engine('sqlite:///restaurantmenu.db')
    # mekes connection between CLASSES and corresponding tables
    Base.metadata.bind = engine
    # establish communication between code and engine
    db_session = sessionmaker(bind = engine)
    # set interface to write all commands in SQL
    # but not send them till nmethod commit() 
    return db_session()


def show_restaurants(rest_ses):
    # check - session query to all Restaurant records
    qr_res = rest_ses.query(Restaurant).all()
    result='Total list of restaurants:\n'
    for item in qr_res:
        result = result + '{} - {}\n'.format(item.id, item.name)
    return result


def add_restaurant(rest_ses):
    # create new record object to table
    new_entry = Restaurant(name = 'Top Burger', 
                        description = 'Home restaurant at the historical center of the town',
                        address = 'Hloria, Middle street, 12')
    # add new element to session staging zone
    rest_ses.add(new_entry)
    # commit changes
    rest_ses.commit()

    # create new record object to table
    new_entry = Restaurant(name = 'Taco Hut', 
                        description = 'Mexican restaurant at the town',
                        address = 'Raho, Central street, 32')
    # add new element to session staging zone
    rest_ses.add(new_entry)
    # commit changes
    rest_ses.commit()


# if mani module to execute
if __name__ == '__main__':
    # set connections
    rest_ses = set_connection()
    # add restaurant
    add_restaurant(rest_ses)
    # print list of restaurants
    print(show_restaurants(rest_ses))


