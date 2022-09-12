
# import flask object and create instance
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)


# 1. Routing for main page - all restaurants list
@app.route('/')
@app.route('/restaurants')
def restaurants():
    return 'Returning list of all restaurants... '

# 1.1. Routing to add restaurant into list
@app.route('/restaurants/add_rst')
def add_restaurant():
    return 'Returning form to add new restaurant... '

# 2. Routing for restaurant info and list of its menu items
# parametrs:
#  - rst_id is path, syntax: rst_idNN where id = NN
@app.route('/restaurants/<string:rst_id>')
def restaurant_id(rst_id):
    return 'Returning menu of reataurant with id: ' + rst_id[6:]

# 2.1. Routing to add menu item to specific restaurant
# parametrs:
#  - rst_id is path, syntax: rst_idNN where id = NN
@app.route('/restaurants/<string:rst_id>/add_mnu')
def add_menu_item_to_restaurant_id(rst_id):
    return 'Returning form to add new menu item to specific restaurant id: ' + rst_id[6:]

# 2.2. Routing to edit menu item id for specific restaurant
# parametrs:
#  - rst_id is path, syntax: rst_idNN where id = NN
#  - mnu_id is path, syntax: mnu_idMM where id = MM
@app.route('/restaurants/<string:rst_id>/<string:mnu_id>/edit')
def edit_menu_item_for_restaurant_id(rst_id, mnu_id):
    return 'Returning form to edit menu item with id: ' + mnu_id[6:] + \
           ' for  specific restaurant id: ' + rst_id[6:]

# 2.3. Routing to delete menu item id for specific restaurant
# parametrs:
#  - rst_id is path, syntax: rst_idNN where id = NN
#  - mnu_id is path, syntax: mnu_idMM where id = MM
@app.route('/restaurants/<string:rst_id>/<string:mnu_id>/delete')
def delete_menu_item_for_restaurant_id(rst_id, mnu_id):
    return 'Returning form to delete menu item with id: ' + mnu_id[6:] + \
           ' for  specific restaurant id: ' + rst_id[6:]

# 2.4. Routing to edit restaurant info
# parametrs:
#  - rst_id is path, syntax: rst_idNN where id = NN
@app.route('/restaurants/<string:rst_id>/edit')
def edit_restaurant_id(rst_id):
    return 'Returning form to edit reataurant with id: ' + rst_id[6:]

# 2.5. Routing to delete restaurant info
# parametrs:
#  - rst_id is path, syntax: rst_idNN where id = NN
@app.route('/restaurants/<string:rst_id>/delete')
def delete_restaurant_id(rst_id):
    return 'Returning form to delete reataurant with id: ' + rst_id[6:]

# 2.6.* Routing to filter restaurant menu items by cource type
# parametrs:
#  - rst_id is path, syntax: rst_idNN where id = NN
@app.route('/restaurants/<string:rst_id>/filter')
def filter_restaurant_id(rst_id):
    return 'Returning form to filter reataurant with id: ' + rst_id[6:]

# 3*. Routing for menu item info
# parametrs:
#  - mnu_id is path, syntax: mnu_idNN where id = NN
@app.route('/restaurants/menu_items/<string:mnu_id>/')
def menu_item_id(mnu_id):
    return 'Returning menu item parameters with id: ' + mnu_id[6:]

# 3.1*. Routing to edit specific menu item info
# parametrs:
#  - mnu_id is path, syntax: mnu_idNN where id = NN
@app.route('/restaurants/menu_items/<string:mnu_id>/edit')
def edit_menu_item_id(mnu_id):
    return 'Returning form to edit menu item with id: ' + mnu_id[6:]

# 3.2*. Routing to delete specific menu item info
# parametrs:
#  - mnu_id is path, syntax: mnu_idNN where id = NN
@app.route('/restaurants/menu_items/<string:mnu_id>/delete')
def delete_menu_item_id(mnu_id):
    return 'Returning form to delete menu item with id: ' + mnu_id[6:]

# 4*. Routing for list of all menu items
@app.route('/restaurants/menu_items/')
def menu_items():
    return 'Returning list of all menu items...  '

# 4.1*. Routing add new menu item
@app.route('/restaurants/menu_items/add')
def add_menu_item():
    return 'Returning form to add new menu item...  '

# if mani module to execute
if __name__ == '__main__':
    # strat debug mode
    app.debug = True
    # run server at port 5000
    app.run(host='0.0.0.0', port=5000)
