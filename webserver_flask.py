
# import flask object and create instance
from flask import Flask, render_template, request, redirect, url_for, \
                  jsonify, flash

# database imports
# Connection to DB and adding information in tables via script
# create_engine will point (connect) to database we used 
from sqlalchemy import create_engine
# import to make connection to 
from sqlalchemy.orm import sessionmaker
# from initial setup module import CLASSES 
from database.database_setup import Base, MenuItem, Restaurant, RestMenuItem

# import os module to check files for logo
# import os.path as path
from os import path
# import os module to get server port
from os import environ


# set_connection:
# set connection to db (from end of CONFIGURATION)
# instance (example) of engine class and connect to database 
engine = create_engine('sqlite:///database/restaurantmenu.db',
                        connect_args={'check_same_thread': False})
# mekes connection between CLASSES and corresponding tables
Base.metadata.bind = engine
# establish communication between code and engine
db_rest_ses = sessionmaker(bind = engine)
# set interface to write all commands in SQL
# but not send them till method commit() 
rest_ses = db_rest_ses()

# instance of Flask object
app = Flask(__name__)


# method to set item attributs via form dictionary
def set_item_attr(add_item, item_dic):
    for (key, item) in item_dic.items():
        try:
            if 'button' in key:         # skip button name key
                continue
            elif item:                  # not empty value - set attribut
                setattr(add_item, key, item)
            else:                       # set attribut to NULL value
                setattr(add_item, key, None)
        except:
            pass
    return add_item

# method to update (not empty) item attributs via form dictionary
def upd_item_attr(add_item, item_dic):
    for (key, item) in item_dic.items():
        try:
            if 'button' in key:             # skip button name key
                continue            
            elif item:                      # not empty value - update attribut
                if item.lower() == 'none':  # update attribut to NULL value
                    setattr(add_item, key, None)
                else:                       # update attribut to entered value
                    setattr(add_item, key, item)
            else:                       # skip empty values
                continue
        except:
            pass
    return add_item


# method to update (not empty) item attributs via form dictionary
def touple_to_dict(keys, tpl_val):
    dict = {}
    idx = 0
    tpl_val_len = len(tpl_val)

    for key in keys:
        if key == '-obj-':                                  # if key is object
            if dict:                                        # if already not empty dic
                obj_items = tpl_val[idx].serialize
                for (o_key, o_val) in obj_items.items():    # hanbdle by object attributes
                    dict[o_key] = o_val
            else:                                           # if  empty dic
                 dict = tpl_val[idx].serialize              # set all object attributes
            idx += 1    
        else:                                               # key is not object
            if idx < tpl_val_len:                           # not all touple values
                dict[key] = tpl_val[idx]
                idx += 1
            else:                                           # all touple values used - empty vals
                dict[key] = '-'

    return dict

# method to create dictionary for message flashing
def gen_responce_dic(pos, clr, msg, id=None):
    return {'position'  : pos,
            'color'     : clr,
            'message'   : msg,
            'id'        : id }

# 1. Routing for main page - all restaurants list

@app.route('/')
@app.route('/api.restaurants/')
@app.route('/restaurants/')
def restaurants():
    # query to get all restaurants
    rest_all_rec = rest_ses.query(Restaurant).all() 
    
    # check logo image files and create list of dictionaries
    rest_rec_logo = []
    for item in rest_all_rec:
        logo_file = item.name.lower().strip(' ').replace(' ','_').replace("'","")+'.jpg'
        # if logo not existed
        if not path.isfile('static/'+ logo_file):
            logo_file = 'no_image.jpg'
        rest_rec_logo.append((item, logo_file))

    # responce: HTML or JSON API
    if 'api.restaurants' in request.path:      # API responce
        RestaurantsJSON = [item.serialize for item in rest_all_rec]
        responce = {'responce type' : 'list of restaurants',
                    'restaurants': RestaurantsJSON }
        return jsonify( responce )
    else:                                       # HTML responce
        return render_template('restaurants.html', rest_items = rest_rec_logo)

    
# 1.1. Routing to add restaurant into list
@app.route('/restaurants/add', methods=['GET', 'POST'])
def add_restaurant():
    # GET method - to send form
    if request.method == 'GET':
        return render_template('add_restaurant.html')        

    # POST method - to recieve data and add to DB
    if request.method == 'POST':
        # add_button pressed - add to DB
        if request.form.get('add_button',0):
            # set new  object attributes and commit
            new_rest =  set_item_attr(Restaurant(), request.form)
            
            try:    # to add new item into DB
                rest_ses.add(new_rest)
                rest_ses.commit()

                # query to get added restaurant with namne and address to open page
                rest_by_id = rest_ses.query(Restaurant).\
                                    filter(Restaurant.name == new_rest.name).\
                                    filter(Restaurant.address == new_rest.address).one()
                
                resp_msg = gen_responce_dic('bottom','confirm_green',
                                            '* Restaurant was added successfully! *')
                flash(resp_msg)
                #redirect to specific restaurant id (to add items)
                return redirect('/restaurants/rst_id{}#top'.format(rest_by_id.id) )
            except: # item not added - redirect to "Add rerstaurant" button
                resp_msg = gen_responce_dic('bottom','reject_red',
                                            '* Restaurant was not added. Try again... *')
                flash(resp_msg)
                # redirect to restaurant list
                return redirect('/restaurants#bottom')     
            
        # cancel_button pressed - redirect to menu items page
        if request.form.get('cancel_button',0):
            return redirect(url_for('restaurants'))           


# 2. Routing for restaurant info and list of its menu items
# parametrs:
#  - rst_id is path, syntax: rst_idNN where id = NN
@app.route('/api.restaurants/<string:rst_id>/')
@app.route('/restaurants/<string:rst_id>/')
def restaurant_id(rst_id):
    try:
        #get restaurant id value
        rst_id_val = int(rst_id[6:])
        # query to get restaurant with id = rst_id_val
        rest_by_id = rest_ses.query(Restaurant).\
                            filter(Restaurant.id == rst_id_val).one()
    except: # url path data for restaurant is incorrect
            # redirect to 'restaurants' page with error message
            resp_msg = gen_responce_dic('top','reject_red',
                                        '* Restaurant was incorrect, select one from the list... *')
            flash(resp_msg)
            return redirect(url_for('restaurants'))

    logo_file = rest_by_id.name.lower().strip(' ').replace(' ','_').replace("'","")+'.jpg'
    # if logo not existed
    if not path.isfile('static/'+ logo_file):
        logo_file = 'no_image.jpg' 

    # select all menu items and prices for restaurant id = rst_id_val
    rest_menu_items_by_id = rest_ses.query(MenuItem,
                                           RestMenuItem.price, RestMenuItem.comment).\
                                     join(MenuItem).\
                                     filter(RestMenuItem.restaurant_id == rst_id_val).\
                                     order_by(MenuItem.course).all()
    
    # responce: HTML or JSON API
    if 'api.restaurants' in request.path:      # API responce
        RestaurantJSON = rest_by_id.serialize 

        keys = ['-obj-', 'price', 'promo comment']
        MenuItemsJSON = []
        for item in rest_menu_items_by_id:
            MenuItemsJSON.append(touple_to_dict(keys, item))

        responce = {'responce type' : 'restaurant menu',
                    'menu items': MenuItemsJSON,
                    'restaurant info' : RestaurantJSON }
        return jsonify( responce )
    else:                                       # HTML responce
        return render_template('restaurant_id.html', rest_item = rest_by_id,
                                menu_items = rest_menu_items_by_id, 
                                logo_name = logo_file)  
    

# 2.1. Routing to add menu item to specific restaurant
# parametrs:
#  - rst_id is path, syntax: rst_idNN where id = NN
@app.route('/restaurants/<string:rst_id>/<string:mnu_id>/add', methods=['GET', 'POST'])
def add_menu_item_to_restaurant_id(rst_id, mnu_id):
    # GET method - to send form
    if request.method == 'GET':
        try:
            #get restaurant id value
            rst_id_val = int(rst_id[6:])
            # query to get restaurant with id = rst_id_val
            rest_by_id = rest_ses.query(Restaurant).\
                            filter(Restaurant.id == rst_id_val).one()
        except: # url path data for restaurant is incorrect
            # redirect to 'restaurants' page with error message
            resp_msg = gen_responce_dic('top','reject_red',
                                        '* Restaurant was incorrect, select one from the list... *')
            flash(resp_msg)
            return redirect(url_for('restaurants'))
        
        try:
            #get menu item id value
            mnu_id_val = int(mnu_id[6:])
            # query to get menu item with id = mnu_id_val
            menu_item_by_id = rest_ses.query(MenuItem).\
                                    filter(MenuItem.id == mnu_id_val).one()
        except:     # url path data for menu item is incorrect
            # redirect to select 'menu items' for specific restaurant with error message
            resp_msg = gen_responce_dic('top','reject_red',
                                        '* Menu item was incorrect, select one from the list... *')
            flash(resp_msg)
            return redirect(url_for('menu_items', rst_id = rst_id))
                            
        return render_template('add_menu_item_to_restaurant_id.html',
                                rest = rest_by_id, item = menu_item_by_id )
           
    if request.method == 'POST':
        # add_button pressed - add to DB
        if request.form.get('add_button',0):
            #get restaurant id value
            rst_id_val = int(rst_id[6:])
            #get menu item id value
            mnu_id_val = int(mnu_id[6:])

            rest_item_dic = {'restaurant_id' : rst_id_val, 
                             'menu_item_id' : mnu_id_val, 
                             'price' : int(request.form['price']), 
                             'comment' : request.form['comment']}

            # set new  object attributes and commit
            new_rest_item =  set_item_attr(RestMenuItem(), rest_item_dic)
            
            try:    # to add new item into DB
                rest_ses.add(new_rest_item)
                rest_ses.commit()       
            
                resp_msg = gen_responce_dic('item','confirm_green',
                                            '* Menu item was added successfully! *', mnu_id_val )
                flash(resp_msg)
                # redirecting to menu item fragment #mid
                return redirect("/restaurants/rst_id{}#m{}".format(rst_id_val, mnu_id_val))
            
            except: # item not added - redirect to "rerstaurant_id" button
                resp_msg = gen_responce_dic('top','reject_red',
                                            '* Menu item was not added. Try again... *')
                flash(resp_msg)
                return redirect(url_for('restaurant_id', rst_id = rst_id))
                                   
        # cancel_button pressed - redirect to menu items page
        if request.form.get('cancel_button',0):
            return redirect(url_for('restaurant_id', rst_id = rst_id))
            

# 2.2. Routing to edit menu item id for specific restaurant
# parametrs:
#  - rst_id is path, syntax: rst_idNN where id = NN
#  - mnu_id is path, syntax: mnu_idMM where id = MM
@app.route('/restaurants/<string:rst_id>/<string:mnu_id>/edit', methods=['GET', 'POST'])
def edit_menu_item_for_restaurant_id(rst_id, mnu_id):
    # GET method - to send form
    if request.method == 'GET':
        try:
            #get restaurant id value
            rst_id_val = int(rst_id[6:])
            # query to get restaurant with id = rst_id_val
            rest_by_id = rest_ses.query(Restaurant).\
                                filter(Restaurant.id == rst_id_val).one()
        except: # url path data for restaurant is incorrect
            # redirect to 'restaurants' page with error message
            resp_msg = gen_responce_dic('top','reject_red',
                                        '* Restaurant was incorrect, select one from the list... *')
            flash(resp_msg)
            return redirect(url_for('restaurants'))

        try:
            #get menu item id value
            mnu_id_val = int(mnu_id[6:])
            # query to get menu item with id = mnu_id_val
            menu_item_by_id = rest_ses.query(MenuItem).\
                                    filter(MenuItem.id == mnu_id_val).one()
        except:     # url path data for menu item is incorrect
            # redirect to 'restaurant_id' page with error message
            resp_msg = gen_responce_dic('top','reject_red',
                                        '* Menu item was incorrect, select one from the list... *')
            flash(resp_msg)
            return redirect(url_for('restaurant_id', rst_id = rst_id))

        # query to get price menu item with restaurant id and  menu item id
        rest_menu_item = rest_ses.query(RestMenuItem).\
                                  filter(RestMenuItem.restaurant_id == rst_id_val).\
                                  filter(RestMenuItem.menu_item_id == mnu_id_val).one()
       
        return render_template('edit_menu_item_for_restaurant_id.html',
                                rest = rest_by_id, item = menu_item_by_id, 
                                rest_item = rest_menu_item )
        
    if request.method == 'POST':
        #get restaurant id value
        rst_id_val = int(rst_id[6:])
        #get menu item id value
        mnu_id_val = int(mnu_id[6:])

        # add_button pressed - add to DB
        if request.form.get('submit_button',0):
            try:
                # query to get price menu item with restaurant id and  menu item id
                rest_menu_item = rest_ses.query(RestMenuItem).\
                                          filter(RestMenuItem.restaurant_id == rst_id_val).\
                                          filter(RestMenuItem.menu_item_id == mnu_id_val).one()
           
                # update object attributes and commit
                rest_menu_item = upd_item_attr(rest_menu_item, request.form)
                rest_ses.add(rest_menu_item)
                rest_ses.commit()
                resp_msg = gen_responce_dic('item','confirm_green',
                                            '* Menu item was updated successfully! *', 
                                            rest_menu_item.menu_item_id)
                flash(resp_msg)
            except: # item not updated
                    resp_msg = gen_responce_dic('item','reject_red',
                                            '* Menu item was not updated. Try again... *',
                                            rest_menu_item.menu_item_id)
                    flash(resp_msg)                   
            # redirecting to menu item fragment #mid
            return redirect("/restaurants/rst_id{}#m{}".format(rst_id_val, mnu_id_val))                      

        if request.form.get('cancel_button',0):
            # redirecting to menu item fragment #mid
            return redirect("/restaurants/rst_id{}#m{}".format(rst_id_val, mnu_id_val))


# 2.3. Routing to delete menu item id for specific restaurant
# parametrs:
#  - rst_id is path, syntax: rst_idNN where id = NN
#  - mnu_id is path, syntax: mnu_idMM where id = MM
@app.route('/restaurants/<string:rst_id>/<string:mnu_id>/delete', methods=['GET', 'POST'])
def delete_menu_item_for_restaurant_id(rst_id, mnu_id):
    # GET method - to send form
    if request.method == 'GET':
        try:
            #get restaurant id value
            rst_id_val = int(rst_id[6:])
            # query to get restaurant with id = rst_id_val
            rest_by_id = rest_ses.query(Restaurant).\
                                filter(Restaurant.id == rst_id_val).one()
        except: # url path data for restaurant is incorrect
            # redirect to 'restaurants' page with error message
            resp_msg = gen_responce_dic('top','reject_red',
                                        '* Restaurant was incorrect, select one from the list... *')
            flash(resp_msg)
            return redirect(url_for('restaurants'))
        
        try:
            # get menu item id value
            mnu_id_val = int(mnu_id[6:])
            # query to get menu item with id = mnu_id_val
            menu_item_by_id = rest_ses.query(MenuItem).\
                                    filter(MenuItem.id == mnu_id_val).one()
        except:     # url path data for menu item is incorrect
            # redirect to 'restaurant_id' page with error message
            resp_msg = gen_responce_dic('top','reject_red',
                                        '* Menu item was incorrect, select one from the list... *')
            flash(resp_msg)
            return redirect(url_for('restaurant_id', rst_id = rst_id))
        
        return render_template('delete_menu_item_for_restaurant_id.html',
                                rest = rest_by_id, item = menu_item_by_id )
        
    if request.method == 'POST':
        #get restaurant id value
        rst_id_val = int(rst_id[6:])
        #get menu item id value
        mnu_id_val = int(mnu_id[6:])

        # add_button pressed - add to DB
        if request.form.get('delete_button',0):
            try:
                # query to get price menu item with restaurant id and  menu item id
                rest_menu_item = rest_ses.query(RestMenuItem).\
                                          filter(RestMenuItem.restaurant_id == rst_id_val).\
                                          filter(RestMenuItem.menu_item_id == mnu_id_val).one()
                # delete price menu item record and commit
                rest_ses.delete(rest_menu_item)
                rest_ses.commit()

                resp_msg = gen_responce_dic('bottom','confirm_green',
                                            '* Menu item was deleted successfully! *')
                flash(resp_msg)
                return redirect('/restaurants/rst_id{}#top'.format(rst_id_val) )
            except: # item not delete
                resp_msg = gen_responce_dic('item','reject_red',
                                            '* Menu item was not delete. Try again... *',
                                            mnu_id_val)
                flash(resp_msg)                   
                # redirecting to menu item fragment #mid
                return redirect("/restaurants/rst_id{}#m{}".format(rst_id_val, mnu_id_val)) 
            
        if request.form.get('cancel_button',0):
            # redirecting to menu item fragment #mid
            return redirect("/restaurants/rst_id{}#m{}".format(rst_id_val, mnu_id_val))
            # return redirect(url_for('restaurant_id', rst_id = rst_id ))           
    

# 2.4. Routing to edit restaurant info
# parametrs:
#  - rst_id is path, syntax: rst_idNN where id = NN
@app.route('/restaurants/<string:rst_id>/edit', methods=['GET', 'POST'])
def edit_restaurant_id(rst_id):
    if request.method == 'GET':
        try:
            #get menu item id value
            rst_id_val = int(rst_id[6:])  
            # query to get restaurant with id = rst_id_val
            rest_by_id = rest_ses.query(Restaurant).\
                                filter(Restaurant.id == rst_id_val).one()
        except: # url path data for restaurant is incorrect
            # redirect to 'restaurants' page with error message
            resp_msg = gen_responce_dic('top','reject_red',
                                        '* Restaurant was incorrect, select one from the list... *')
            flash(resp_msg)
            return redirect(url_for('restaurants'))
        
        return render_template('edit_restaurant_id.html',  rest = rest_by_id )
        
    if request.method == 'POST':
        if request.form.get('submit_button',0):
            #get menu item id value
            rst_id_val = int(rst_id[6:])
            
            try:
                # query to get restaurant with id = rst_id_val
                rest_by_id = rest_ses.query(Restaurant).\
                                      filter(Restaurant.id == rst_id_val).one()
            
                # update object attributes and commit
                rest_by_id =  upd_item_attr(rest_by_id, request.form)
                rest_ses.add(rest_by_id)
                rest_ses.commit() 

                resp_msg = gen_responce_dic('bottom','confirm_green',
                                            '* Restaurant was updated successfully! *')
                flash(resp_msg)
            except: # restaurant not updated
                    resp_msg = gen_responce_dic('bottom','reject_red',
                                            '* Restaurant was not updated. Try again... *')
                    flash(resp_msg)

            # redirect to 'restaurant id" page           
            return redirect('/restaurants/rst_id{}#top'.format(rst_id_val) )
                    
        if request.form.get('cancel_button',0):
            return redirect(url_for('restaurant_id', rst_id = rst_id ))
            

# 2.5. Routing to delete restaurant info
# parametrs:
#  - rst_id is path, syntax: rst_idNN where id = NN
@app.route('/restaurants/<string:rst_id>/delete', methods=['GET', 'POST'])
def delete_restaurant_id(rst_id):
    if request.method == 'GET':
        try:
            #get menu item id value
            rst_id_val = int(rst_id[6:]) 
            # query to get restaurant with id = rst_id_val
            rest_by_id = rest_ses.query(Restaurant).\
                                filter(Restaurant.id == rst_id_val).one()
        except: # url path data for restaurant is incorrect
            # redirect to 'restaurants' page with error message
            resp_msg = gen_responce_dic('top','reject_red',
                                        '* Restaurant was incorrect, select one from the list... *')
            flash(resp_msg)
            return redirect(url_for('restaurants'))
        
        # query to get price menu item with restaurant id 
        rest_menu_items = rest_ses.query(RestMenuItem.menu_item_id, MenuItem.name ).\
                                   join(MenuItem).\
                                   filter(RestMenuItem.restaurant_id == rst_id_val).all()
        
        return render_template('delete_restaurant_id.html',  rest = rest_by_id, 
                                mnu_itms_qnt = rest_menu_items)
            
    if request.method == 'POST':
        if request.form.get('delete_button',0):
            #get menu item id value
            rst_id_val = int(rst_id[6:])         
            # query to get all records with restaurant id from RestMenuItem table
            rest_menu_items = rest_ses.query(RestMenuItem).\
                                          filter(RestMenuItem.restaurant_id == rst_id_val).all()
            
            # if restaurant have menu items - delete records from RestMenuItem
            if rest_menu_items:
                try:
                    # delete selected records from RestMenuItem table
                    for item in rest_menu_items:
                        rest_ses.delete(item)
                    rest_ses.commit()  
                except: # items not deleted - redirect to "restaurant id" page
                    resp_msg = gen_responce_dic('bottom','reject_red',
                                            '* Restaurant was not deleted. Try again... *')
                    flash(resp_msg)
                    # redirecting to restaurant with error message    
                    return redirect('/restaurants/rst_id{}#top'.format(rst_id_val) )
                  
            try:
                # query to get restaurant with id = rst_id_val
                rest_by_id = rest_ses.query(Restaurant).\
                                      filter(Restaurant.id == rst_id_val).one()
                # delete restaurant record and commit
                rest_ses.delete(rest_by_id)
                rest_ses.commit()

                resp_msg = gen_responce_dic('top','confirm_green',
                                            '* Restaurant was deleted successfully! *')
                flash(resp_msg)
                # redirecting to restaurants list
                return redirect(url_for('restaurants'))
            
            except: # item not deleted - redirect to "menu item id" page
                resp_msg = gen_responce_dic('bottom','reject_red',
                                            '* Menu items were deleted, \
                                               but not restaurant. Try again... *')
                flash(resp_msg)
                # redirecting to item with error message
                return redirect('/restaurants/rst_id{}#top'.format(rst_id_val) ) 
            
        if request.form.get('cancel_button',0):
            return redirect(url_for('restaurant_id', rst_id = rst_id ))   
    

# 2.6*. Routing to filter restaurant menu items by cource type
# parametrs:
#  - rst_id is path, syntax: rst_idNN where id = NN
@app.route('/restaurants/<string:rst_id>/filter')
def filter_restaurant_id(rst_id):
    return '2.6*. Returning form to filter reataurant with id: ' + rst_id[6:]
    

# 3*. Routing for menu item info
# parametrs:
#  - mnu_id is path, syntax: mnu_idNN where id = NN
@app.route('/restaurants/menu_items/<string:mnu_id>')
@app.route('/restaurants/<string:rst_id>/<string:mnu_id>')
def menu_item_id(mnu_id, rst_id=None):
    #get restaurant id value if possible
    if rst_id:
        try:
            rst_id_val = int(rst_id[6:])
            # query to get restaurant with id = rst_id_val
            restaurant = rest_ses.query(Restaurant).\
                                filter(Restaurant.id == rst_id_val).one()
        except: # url path data for restaurant is incorrect
            # redirect to 'restaurants' page with error message
            resp_msg = gen_responce_dic('top','reject_red',
                                        '* Restaurant was incorrect, select one from the list... *')
            flash(resp_msg)
            return redirect(url_for('restaurants')) 
    else:
        restaurant = None   
    
    try:
        #get menu item id value
        mnu_id_val = int(mnu_id[6:])
        # query to get menu item with id = mnu_id_val
        mnu_by_id = rest_ses.query(MenuItem).\
                            filter(MenuItem.id == mnu_id_val).one()
    except:     # url path data for menu item is incorrect
        # redirect to 'menu items' or 'restaurant_id' page with error message
        resp_msg = gen_responce_dic('top','reject_red',
                                    '* Menu item was incorrect, select one from the list... *')
        flash(resp_msg)
        if rst_id:
            return redirect(url_for('restaurant_id', rst_id = rst_id ))
        else:
            return redirect(url_for('menu_items')) 

    return render_template('menu_item_id.html', menu_item = mnu_by_id,
                            rest_item = restaurant)    
    

# 3.1*. Routing to edit specific menu item info
# parametrs:
#  - mnu_id is path, syntax: mnu_idNN where id = NN
@app.route('/restaurants/menu_items/<string:mnu_id>/edit', methods=['GET', 'POST'])
def edit_menu_item_id(mnu_id):
    if request.method == 'GET':
        try:
            #get menu item id value
            mnu_id_val = int(mnu_id[6:])  
            # query to get menu item with id = mnu_id_val
            mnu_by_id = rest_ses.query(MenuItem).\
                                filter(MenuItem.id == mnu_id_val).one()
        except:     # url path data for menu item is incorrect
            # redirect to 'menu items' page with error message
            resp_msg = gen_responce_dic('top','reject_red',
                                        '* Menu item was incorrect, select one from the list... *')
            flash(resp_msg)
            return redirect(url_for('menu_items'))
        
        return render_template('edit_menu_item_id.html',  menu_item = mnu_by_id )        

    if request.method == 'POST':
        if request.form.get('submit_button',0):
            #get menu item id value
            mnu_id_val = int(mnu_id[6:])
            
            try:
                # query to get menu item with id = mnu_id_val
                menu_by_id = rest_ses.query(MenuItem).\
                                      filter(MenuItem.id == mnu_id_val).one()
            
                # update object attributes and commit
                menu_by_id =  upd_item_attr(menu_by_id, request.form)
                rest_ses.add(menu_by_id)
                rest_ses.commit() 
                
                resp_msg = gen_responce_dic('bottom','confirm_green',
                                            '* Menu item was updated successfully! *')
                flash(resp_msg)
            except: # item not updated
                    resp_msg = gen_responce_dic('bottom','reject_red',
                                            '* Menu item was not updated. Try again... *')
                    flash(resp_msg)

            # redirect to "menu item id" page
            return redirect(url_for('menu_item_id', mnu_id = mnu_id ))
                   
        if request.form.get('cancel_button',0):
            return redirect(url_for('menu_item_id', mnu_id = mnu_id ))            


# 3.2*. Routing to delete specific menu item info
# parametrs:
#  - mnu_id is path, syntax: mnu_idNN where id = NN
@app.route('/restaurants/menu_items/<string:mnu_id>/delete', methods=['GET', 'POST'])
def delete_menu_item_id(mnu_id):
    if request.method == 'GET':
        try:
            #get menu item id value
            mnu_id_val = int(mnu_id[6:])
            # query to get menu item with id = mnu_id_val
            menu_by_id = rest_ses.query(MenuItem).\
                                filter(MenuItem.id == mnu_id_val).one()
        except:     # url path data for menu item is incorrect
            # redirect to 'menu items' page with error message
            resp_msg = gen_responce_dic('top','reject_red',
                                        '* Menu item was incorrect, select one from the list... *')
            flash(resp_msg)
            return redirect(url_for('menu_items'))

        # query to get all restaurants with menu item id from RestMenuItem table
        rest_menu_item_id = rest_ses.query(RestMenuItem.restaurant_id, Restaurant.name).\
                                      join(Restaurant).\
                                      filter(RestMenuItem.menu_item_id == mnu_id_val).all()

        return render_template('delete_menu_item_id.html',  menu_item = menu_by_id,
                                rest_lst = rest_menu_item_id)        
    
    if request.method == 'POST':
        if request.form.get('delete_button',0):
            #get menu item id value
            mnu_id_val = int(mnu_id[6:])
            # query to get all records with menu item id = mnu_id_val
            rest_menu_by_id = rest_ses.query(RestMenuItem).\
                                      filter(RestMenuItem.menu_item_id == mnu_id_val).all()
           
            # if menu item is used at restaurants - delete records from RestMenuItem
            if rest_menu_by_id:
                try:   
                    # delete selected records from RestMenuItem table
                    for item in rest_menu_by_id:
                        rest_ses.delete(item)
                    rest_ses.commit()
                except: # item not deleted - redirect to "menu item id" page
                    resp_msg = gen_responce_dic('bottom','reject_red',
                                            '* Menu item was not deleted. Try again... *')
                    flash(resp_msg)
                    # redirecting to item with error message
                    return redirect(url_for('menu_item_id', mnu_id = mnu_id ))
                      
            try:    
                # query to get menu item with id = mnu_id_val
                menu_by_id = rest_ses.query(MenuItem).\
                                      filter(MenuItem.id == mnu_id_val).one()
                # delete selected record from MenuItem table
                rest_ses.delete(menu_by_id)
                rest_ses.commit() 

                resp_msg = gen_responce_dic('top','confirm_green',
                                            '* Menu item was deleted successfully! *')
                flash(resp_msg)
                # redirecting to item list
                return redirect(url_for('menu_items')) 
            except: # item not deleted - redirect to "menu item id" page
                resp_msg = gen_responce_dic('bottom','reject_red',
                                            '* Menu item was deleted from restaurants, \
                                               but not from menu list. Try again... *')
                flash(resp_msg)
                # redirecting to item with error message
                return redirect(url_for('menu_item_id', mnu_id = mnu_id ))          

        if request.form.get('cancel_button',0):
            return redirect(url_for('menu_item_id', mnu_id = mnu_id ))           


# 4*. Routing for list of all menu items
@app.route('/api.restaurants/menu_items/')
@app.route('/restaurants/menu_items/')
@app.route('/restaurants/menu_items/<string:rst_id>/add')
def menu_items(rst_id = None):   
    if rst_id:                      # adding not existed menu items to restaurant
        try:
            #get menu item id value
            rst_id_val = int(rst_id[6:])    
            # query to get restaurant with id = rst_id_val
            restaurant = rest_ses.query(Restaurant).\
                                filter(Restaurant.id == rst_id_val).one()
        except: # url path data for restaurant is incorrect
            # redirect to 'restaurants' page with error message
            resp_msg = gen_responce_dic('top','reject_red',
                                        '* Restaurant was incorrect, select one from the list... *')
            flash(resp_msg)
            return redirect(url_for('restaurants'))
        
        # query to get all menu item ids for sprcific restaurant id from RestMenuItem
        rest_id_menu_items = rest_ses.query(RestMenuItem.menu_item_id).\
                                      filter(RestMenuItem.restaurant_id == rst_id_val).all()
        
        # select all menu item id's not existed in restaurant id to filter for adding       
        if rest_id_menu_items:  # if not empty create list of menu item ids existed
            mnu_itms_ids = [ a for (a,) in rest_id_menu_items ]
           
            # query to get menu items with ids not existed for restaurant id 
            no_menu_item_lst = rest_ses.query(MenuItem).\
                                        filter(~MenuItem.id.in_(mnu_itms_ids)).\
                                        order_by(MenuItem.course).all()
        else:                   # no menu - select all menu items
            no_menu_item_lst = rest_ses.query(MenuItem).order_by(MenuItem.course).all()
       
        return render_template('menu_items.html', menu_items = no_menu_item_lst,
                                rest = restaurant)      
    else:                           # show all menu items 
        rst_itm = None
        # query to get all menu items
        menu_items_all_rec = rest_ses.query(MenuItem).order_by(MenuItem.course).all() 

        # responce: HTML or JSON API
        if 'api.restaurants' in request.path:      # API responce
            MenuItemsJSON = [item.serialize for item in menu_items_all_rec]
            responce = {'responce type' : 'list of menu items',
                        'menu items': MenuItemsJSON}
            return jsonify( responce )
        else:                                       # HTML responce
            return render_template('menu_items.html', menu_items = menu_items_all_rec,
                                    rest = rst_itm) 
     

# 4.1*. Routing to add new menu item
@app.route('/restaurants/menu_items/add', methods=['GET', 'POST'])
def add_menu_item():
    # GET method - to send form
    if request.method == 'GET':
        return render_template('add_menu_item.html')        

    # POST method - to recieve data and add to DB
    if request.method == 'POST':
        # add_button pressed - add to DB
        if request.form.get('add_button',0):
            # set new  object attributes and commit
            new_item =  set_item_attr(MenuItem(), request.form)
            
            try:    # to add new item into DB
                rest_ses.add(new_item)
                rest_ses.commit() 

                # query to select item id
                menu_by_id = rest_ses.query(MenuItem).\
                                      filter(MenuItem.name == new_item.name).\
                                      filter(MenuItem.description == new_item.description).one()            
                
                resp_msg = gen_responce_dic('item','confirm_green',
                                            '* Menu item was added successfully! *', menu_by_id.id )
                flash(resp_msg)
                return redirect('/restaurants/menu_items#m{}'.format(menu_by_id.id))               
            except:
                resp_msg = gen_responce_dic('bottom','reject_red',
                                            '* Menu item was not added. Try again... *')
                flash(resp_msg)
                return redirect(url_for('menu_items'))   

        # cancel_button pressed - redirect to menu items page
        if request.form.get('cancel_button',0):
            return redirect(url_for('menu_items')) 


# 5*. Routing to show 'News & Promo' page
@app.route('/api.restaurants/news_promo')
@app.route('/restaurants/news_promo')
def news_promo():
    # select all menu and restaurant from RestMenuItem for filtering where 'comment' not None
    all_promo_lst = rest_ses.query(Restaurant.name, MenuItem.name, \
                                   RestMenuItem.price, RestMenuItem.comment, \
                                   RestMenuItem.restaurant_id).\
                             join(MenuItem).join(Restaurant).\
                             filter(RestMenuItem.comment != None).\
                             order_by(Restaurant.id, MenuItem.id).all()

     # if 'promo' records are existed    
    if all_promo_lst:
        # check logo image files and create list of dictionaries
        all_promo_lst_logo = []
        for item in all_promo_lst:
            logo_file = item[0].lower().strip(' ').replace(' ','_').replace("'","")+'.jpg'
            # if logo not existed
            if not path.isfile('static/'+ logo_file):
                logo_file = 'no_image.jpg'
            all_promo_lst_logo.append((item, logo_file))  
    else:
          all_promo_lst_logo = []

    # responce: HTML or JSON API
    if 'api.restaurants' in request.path:      # API responce
        keys = ['restaurant', 'menu item', 'price', 'promo comment']
        MenuItemsJSON = []
        for item in all_promo_lst:
            MenuItemsJSON.append(touple_to_dict(keys, item))

        responce = {'responce type' : 'list of promo menu items',
                    'promo items': MenuItemsJSON}
        return jsonify( responce )
    else:                                       # HTML responce
        return render_template('news_promo.html', promo_lst = all_promo_lst_logo)

    
# 6*. Routing to show 'Contact us' page
@app.route('/restaurants/contact_us')
def contact_us():
    return render_template('contact_us.html')
        
        
# if mani module to execute
if __name__ == '__main__':
    # set key for flashing
    app.secret_key = 'Add#flash*key_10'
    # strat debug mode
    app.debug = True
    # run server at current port from os.environ 
    # or default port 5000
    os_port = int(environ.get('PORT', 5000))   # Use PORT if it's there.
    app.run(host='0.0.0.0', port=os_port)



