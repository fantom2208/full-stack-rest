# inserting data to table restaurant module

# Connection to DB and adding information in tables via script
# create_engine will point (connect) to database we used 
from sqlalchemy import create_engine
# import to make connection to 
from sqlalchemy.orm import sessionmaker
# from initial setup module import CLASSES 
from database_setup import Base, MenuItem, Restaurant, RestMenuItem


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


def show_restaurants(rest_ses):
    # check - session query to all Restaurant records
    qr_res = rest_ses.query(Restaurant).all()
    result='Total list of restaurants:\n'
    for item in qr_res:
        result = result + '{} - {}\n'.format(item.id, item.name)
    return result


def show_rest_menu_items(rest_ses):
    # check - session query to all Restaurant records
    qr_res = rest_ses.query(RestMenuItem).all()
    result='Total list of menu items prices:\n'
    for item in qr_res:
        result = result + '{} - {} - {} - {}\n'.format(item.id, item.restaurant_id, item.menu_item_id, item.price)
    return result  

def add_menu_item_prices(rest_ses):
    # create new record object to table
    new_rest = Restaurant(name = 'Blue Burgers', 
                        description = 'Nice restaurant at the town',
                        address = 'Georgia, Central square, 2')
    # add new element to session staging zone
    rest_ses.add(new_rest)
    # commit changes
    rest_ses.commit()

    # check - session query to all Restaurant records
    print(show_restaurants(rest_ses))

    # create new record object to table
    new_item = MenuItem(name = 'Chocolate Cake',
                        description = 'made with Dutch Chocolate',
                        course = 'Dessert',
                        weight = 100,
                        content = '')
    # add new element to rest_ses staging zone
    rest_ses.add(new_item)

    new_item = MenuItem(name = "Mushroom risotto", 
                        description = "Portabello mushrooms in a creamy risotto", 
                        course = "Entree", 
                        weight = 300)
    # add new element to rest_ses staging zone
    rest_ses.add(new_item)
    # commit changes
    rest_ses.commit()

    # check - session query to all MenuItem records
    print(show_menu_items(rest_ses))


    # add menu to restaurant by objects
    NewMenuItem = RestMenuItem(restaurant = new_rest, 
                            menu_item = new_item, 
                            price = 750, 
                            comment = "New taste for this summer!" )
    rest_ses.add(NewMenuItem)
    #rest_ses.commit()

    # add menu to restaurant by restaurant object and menu item id
    MenuItem1 = RestMenuItem(restaurant = new_rest, 
                            menu_item_id = 2, 
                            price = 550)
    rest_ses.add(MenuItem1)
    # rest_ses.commit()

    # add menu to restaurant by restaurant and menu item ids
    MenuItem2 = RestMenuItem(restaurant_id = 3, 
                            menu_item_id = 1, 
                            price = 650)
    rest_ses.add(MenuItem2)
    rest_ses.commit()

    # add menu to restaurant by restaurant (id=1) and menu item ids
    AddMenuItem = RestMenuItem(restaurant_id = 1, 
                            menu_item_id = 3, 
                            price = 400)
    rest_ses.add(AddMenuItem)

    AddMenuItem = RestMenuItem(restaurant_id = 1, 
                            menu_item_id = 4, 
                            price = 250)
    rest_ses.add(AddMenuItem)

    AddMenuItem = RestMenuItem(restaurant_id = 1, 
                            menu_item_id = 5, 
                            price = 550)
    rest_ses.add(AddMenuItem)

    AddMenuItem = RestMenuItem(restaurant_id = 1, 
                            menu_item_id = 6, 
                            price = 450)
    rest_ses.add(AddMenuItem)
    rest_ses.commit()

    

# if mani module to execute
if __name__ == '__main__':
    # set connections
    rest_ses = set_connection()
    # add restaurant
    add_menu_item_prices(rest_ses)
    # print list of restaurants
    print(show_rest_menu_items(rest_ses))

