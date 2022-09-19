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
    db_rest_ses = sessionmaker(bind = engine)
    # set interface to write all commands in SQL
    # but not send them till nmethod commit() 
    return db_rest_ses()


def show_menu_items(rest_ses):
    # check - session query to all Restaurant records
    qr_res = rest_ses.query(MenuItem).all()
    result='Total list of menu items:\n'
    for item in qr_res:
        result = result + '{} - {} - {}\n'.format(item.id, item.name, item.description)
    return result


def add_menu_items(rest_ses):
    # create new record object to table
    new_item = MenuItem(name = 'Pizza cheese', 
                        description = 'Nice pizza with Mozzarella and Lamber, D = 42 cm',
                        course = 'Entree',
                        weight = 800,
                        content = 'Flour, water, salt, tomato souce, Mozzarella and Lamber cheeses')
    # add new element to rest_ses staging zone
    rest_ses.add(new_item)
    # commit changes
    rest_ses.commit()

    # check - session query to all MenuItem records
    # print(show_menu_items(rest_ses))


    menuItem2 = MenuItem(name = "Veggie Burger", 
                        description = "Juicy grilled veggie patty with tomato mayo and lettuce", 
                        course = "Entree",
                        weight = 400)
    rest_ses.add(menuItem2)
    #rest_ses.commit()

    menuItem1 = MenuItem(name = "French Fries", 
                        description = "with garlic and parmesan", 
                        course = "Appetizer", 
                        weight = 200,
                        content = 'Potatos, sunflower oil')
    rest_ses.add(menuItem1)
    #rest_ses.commit()

    menuItem2 = MenuItem(name = "Chicken Burger", 
                        description = "Juicy grilled chicken patty with tomato mayo and lettuce", 
                        course = "Entree",
                        weight = 350)
    rest_ses.add(menuItem2)
    rest_ses.commit()



# if mani module to execute
if __name__ == '__main__':
    # set connections
    rest_ses = set_connection()
    # add restaurant
    add_menu_items(rest_ses)
    # print list of restaurants
    print(show_menu_items(rest_ses))

