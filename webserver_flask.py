
# import flask object and create instance
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

# print('-----------')
# cont = vars(app)
# for key,item in cont.items():
#     print(key, '-', item)
# print('-----------')

# dummy variables to simulate ORM functioning
# Restaurants (list of objects)
restaurant_lst = [{'id': 1,
                 'name' : 'Top Burger', 
                 'description' : 'Home restaurant at the historical center of the town',
                 'address' : 'Hloria, Middle street, 12'}, 
                {'name':'Blue Burgers', 
                 'description' : 'Nice restaurant at the town',
                 'address' : 'Georgia, Central square, 2',
                 'id': 2},
                {'name':'Taco Hut', 
                 'description' : 'Mexican restaurant at the town',
                 'address' : 'Raho, Central street, 3',          
                 'id': 3}]
# Menu Items (list of objects)
menu_item_lst = [{'name':'Cheese Pizza',
                 'description':'made with fresh cheese',
                 'course' :'Entree',
                 'weight' : 800,
                 'content' : 'Flour, water, salt, tomato souce, Mozzarella and Lamber cheeses',
                 'id': 1},
                {'name':'Chocolate Cake',
                 'description':'made with Dutch Chocolate',
                 'course':'Dessert',
                 'weight' : 100,
                 'content' : '',
                 'id': 2},
                {'name':'Caesar Salad', 
                 'description':'with fresh organic vegetables',
                 'course':'Entree',
                 'weight' : 250,
                 'content' : '',
                 'id': 3},
                {'name':'Iced Tea', 
                 'description':'with lemon',
                 'course':'Beverage',
                 'weight' : 200,
                 'content' : '',
                 'id': 4},
                {'name':'Spinach Dip', 
                 'description':'creamy dip with fresh spinach',
                 'weight' : 100,
                 'content' : '',                 
                 'course':'Appetizer','id': 5}]
# Menu Items Prices (list of objects)
rest_menu_item_lst = [{'restaurant_id' : 1, 
                     'menu_item_id' : 1, 
                     'price' : 750, 
                     'comment' : "New taste for this summer!",
                     'id': 1},
                    {'restaurant_id' : 1, 
                     'menu_item_id' : 3, 
                     'price' : 350, 
                     'comment' : "Fresh vegatables",
                     'id': 2},
                    {'restaurant_id' : 1, 
                     'menu_item_id' : 5, 
                     'price' : 150, 
                     'comment' : '',
                     'id': 3}, 
                    {'restaurant_id' : 2, 
                     'menu_item_id' : 2, 
                     'price' : 250, 
                     'comment' : '',
                     'id': 4},
                    {'restaurant_id' : 2, 
                     'menu_item_id' : 4, 
                     'price' : 150, 
                     'comment' : '',
                     'id': 5},
                    {'restaurant_id' : 2, 
                     'menu_item_id' : 1, 
                     'price' : 600, 
                     'comment' : 'Promo price',
                     'id': 6}]


# dummy function to simulate query of getting restaurant item by restaurant id
def query_restaurants(rest_id):
    for item in restaurant_lst:
        if item['id'] == rest_id:
            return item

# dummy function to simulate query of getting menu_item by id
def query_menu_items(mnu_id):
    for item in menu_item_lst:
        if item['id'] == mnu_id:
            return item

# dummy function to simulate query of getting menu item by menu item id list
def query_list_menu_items(rst_mnu_itms):
    query_list = []
    for item in rst_mnu_itms:
        for memu in menu_item_lst:
            if memu['id'] == item['menu_item_id']:
                query_list.append(memu)
                # print(memu)
    return query_list


# dummy function to simulate query of getting menu items by restaurant id
def query_list_rest_menu_items_by_rst(rest_id):
    query_list = []
    for item in rest_menu_item_lst:
        if item['restaurant_id'] == rest_id:
            query_list.append(item)
            # print(item)
    return query_list

# dummy function to simulate query of getting menu items by restaurant id
def query_list_rest_menu_items_by_mnu(mnu_id):
    query_list = []
    for item in rest_menu_item_lst:
        if item['menu_item_id'] == mnu_id:
            query_list.append(item)
            # print(item)
    return query_list

# 1. Routing for main page - all restaurants list
@app.route('/')
@app.route('/restaurants/')
def restaurants():
    return render_template('restaurants.html', rest_items = restaurant_lst)
    # return '1. Returning list of all restaurants... '

# 1.1. Routing to add restaurant into list
@app.route('/restaurants/add', methods=['GET', 'POST'])
def add_restaurant():
    # GET method - to send form
    if request.method == 'GET':
        return render_template('add_restaurant.html')
        # return '1.1*. Returning form to add new restaurant... 

    # POST method - to recieve data and add to DB
    if request.method == 'POST':
        # add_button pressed - add to DB
        if request.form.get('add_button',0):
            new_restaurant = {'name' : request.form['name'], 
                              'description' : request.form['description'], 
                              'address' : request.form['address'], 
                              'id' : len(restaurant_lst) + 1}

            restaurant_lst.append(new_restaurant)
	        # new_menu_item = MenuItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], course = request.form['course'], restaurant_id = restaurant_id)
            # session.add(newItem)
	        # session.commit()
            return redirect(url_for('restaurant_id', rst_id = 'rst_id{}'.format(new_restaurant['id']) ))
            # return '1.1*. Redirecting to page with new restaurant...  

        # cancel_button pressed - redirect to menu items page
        if request.form.get('cancel_button',0):
            return redirect(url_for('restaurants'))
            # return '1.1*. Redirecting to page with all restaurants...     


# 2. Routing for restaurant info and list of its menu items
# parametrs:
#  - rst_id is path, syntax: rst_idNN where id = NN
@app.route('/restaurants/<string:rst_id>/')
def restaurant_id(rst_id):
    #get restaurant id value
    rst_id_val = int(rst_id[6:])

    #simulate "dummy" queries to get data by restaurant id
    restaurant = query_restaurants(rst_id_val)
    rest_menu_items = query_list_rest_menu_items_by_rst(rst_id_val)
    ftrd_menu_items = query_list_menu_items(rest_menu_items)

    return render_template('restaurant_id.html', rest_item = restaurant,
                            mnu_itm_prs = rest_menu_items, mnu_itms = ftrd_menu_items)
    # return '2. Returning menu of reataurant with id: ' + rst_id[6:]

# 2.1. Routing to add menu item to specific restaurant
# parametrs:
#  - rst_id is path, syntax: rst_idNN where id = NN
@app.route('/restaurants/<string:rst_id>/add')
def add_menu_item_to_restaurant_id(rst_id):
    return '2.1. Returning form to add new menu item to specific restaurant id: ' + rst_id[6:]

# 2.2. Routing to edit menu item id for specific restaurant
# parametrs:
#  - rst_id is path, syntax: rst_idNN where id = NN
#  - mnu_id is path, syntax: mnu_idMM where id = MM
@app.route('/restaurants/<string:rst_id>/<string:mnu_id>/edit')
def edit_menu_item_for_restaurant_id(rst_id, mnu_id):
    return '2.2. Returning form to edit menu item with id: ' + mnu_id[6:] + \
           ' for  specific restaurant id: ' + rst_id[6:]

# 2.3. Routing to delete menu item id for specific restaurant
# parametrs:
#  - rst_id is path, syntax: rst_idNN where id = NN
#  - mnu_id is path, syntax: mnu_idMM where id = MM
@app.route('/restaurants/<string:rst_id>/<string:mnu_id>/delete')
def delete_menu_item_for_restaurant_id(rst_id, mnu_id):
    return '2.3. Returning form to delete menu item with id: ' + mnu_id[6:] + \
           ' for  specific restaurant id: ' + rst_id[6:]

# 2.4. Routing to edit restaurant info
# parametrs:
#  - rst_id is path, syntax: rst_idNN where id = NN
@app.route('/restaurants/<string:rst_id>/edit', methods=['GET', 'POST'])
def edit_restaurant_id(rst_id):
    if request.method == 'GET':
        #get menu item id value
        rst_id_val = int(rst_id[6:])    
        rst_itm = query_restaurants(rst_id_val)
        return render_template('edit_restaurant_id.html',  rest = rst_itm )
        #return '2.4. Returning form to edit reataurant with id: ' + rst_id[6:]

    if request.method == 'POST':
        if request.form.get('submit_button',0):
            #get menu item id value
            rst_id_val = int(rst_id[6:])

            rst_itm = query_restaurants(rst_id_val)
            rst_itm_idx = restaurant_lst.index(rst_itm)

            if request.form['name']:
                restaurant_lst[rst_itm_idx]['name'] = request.form['name']
            if request.form['description']:
                restaurant_lst[rst_itm_idx]['description'] = request.form['description']
            if request.form['address']:
                restaurant_lst[rst_itm_idx]['address'] = request.form['address']  
                       
            return redirect(url_for('restaurant_id', rst_id = rst_id ))
            #  return '2.4*. Redirecting to page with restaurant id: ' + rst_id[6:] 
        
        if request.form.get('cancel_button',0):
            return redirect(url_for('restaurant_id', rst_id = rst_id ))
            # return '2.4*. Redirecting to page with restaurant id: ' + rst_id[6:]  


# 2.5. Routing to delete restaurant info
# parametrs:
#  - rst_id is path, syntax: rst_idNN where id = NN
@app.route('/restaurants/<string:rst_id>/delete', methods=['GET', 'POST'])
def delete_restaurant_id(rst_id):
    if request.method == 'GET':
        #get menu item id value
        rst_id_val = int(rst_id[6:])    
        rst_itm = query_restaurants(rst_id_val)

        # get menu item quantity for specific restaurant
        rest_menu_items = query_list_rest_menu_items_by_rst(rst_id_val)

        return render_template('delete_restaurant_id.html',  rest = rst_itm, 
                                mnu_itms_qnt = len(rest_menu_items))
        #return '2.5. Returning form to delete reataurant with id: ' + rst_id[6:]
    
    if request.method == 'POST':
        if request.form.get('delete_button',0):
            #get menu item id value
            rst_id_val = int(rst_id[6:]) 

            # delete all records from RestMenuItem table
            idx = 0
            while idx < len(rest_menu_item_lst):
                if rest_menu_item_lst[idx]['restaurant_id'] == rst_id_val:
                    # print('------\n', rest_menu_item_lst[idx])
                    rest_menu_item_lst.pop(idx)
                else:
                    idx += 1

            rst_itm = query_restaurants(rst_id_val)
            rst_itm_idx = restaurant_lst.index(rst_itm)
            restaurant_lst.pop(rst_itm_idx)
            return redirect(url_for('restaurants'))
            # return '3.2*. Redirecting to page with all restaurantss...

        if request.form.get('cancel_button',0):
            return redirect(url_for('restaurant_id', rst_id = rst_id ))
            # return '2.5*. Redirecting to page with restaurant id: ' + rst_id[6:]
    
    

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
    #get menu item id value
    mnu_id_val = int(mnu_id[6:])
    mnu_itm = query_menu_items(mnu_id_val)

    #get restaurant id value if possible
    if rst_id:
        rst_id_val = int(rst_id[6:])
        restaurant = query_restaurants(rst_id_val)
    else:
        restaurant = None
    
    return render_template('menu_item_id.html', menu_item = mnu_itm,
                            rest_item = restaurant)
    # return '3*. Returning menu item parameters with id: ' + mnu_id[6:]

# 3.1*. Routing to edit specific menu item info
# parametrs:
#  - mnu_id is path, syntax: mnu_idNN where id = NN
@app.route('/restaurants/menu_items/<string:mnu_id>/edit', methods=['GET', 'POST'])
def edit_menu_item_id(mnu_id):
    if request.method == 'GET':
        #get menu item id value
        mnu_id_val = int(mnu_id[6:])    
        mnu_itm = query_menu_items(mnu_id_val)
        return render_template('edit_menu_item_id.html',  menu_item = mnu_itm )
        # return '3.1*. Returning form to edit menu item with id: ' + mnu_id[6:]

    if request.method == 'POST':
        if request.form.get('submit_button',0):
            #get menu item id value
            mnu_id_val = int(mnu_id[6:])

            mnu_itm = query_menu_items(mnu_id_val)
            mnu_itm_idx = menu_item_lst.index(mnu_itm)

            if request.form['name']:
                menu_item_lst[mnu_itm_idx]['name'] = request.form['name']
            if request.form['description']:
                menu_item_lst[mnu_itm_idx]['description'] = request.form['description']
            if request.form['course']:
                menu_item_lst[mnu_itm_idx]['course'] = request.form['course']  
            if request.form['weight']:
                menu_item_lst[mnu_itm_idx]['weight'] = request.form['weight'] 
            if request.form['content']:
                menu_item_lst[mnu_itm_idx]['content'] = request.form['content']  
            
            return redirect(url_for('menu_item_id', mnu_id = mnu_id ))
            #  return '3.1*. Redirecting to page with menu item with id: ' + mnu_id[6:] 
        
        if request.form.get('cancel_button',0):
            return redirect(url_for('menu_item_id', mnu_id = mnu_id ))
            #  return '3.1*. Redirecting to page with menu item with id: ' + mnu_id[6:]     


# 3.2*. Routing to delete specific menu item info
# parametrs:
#  - mnu_id is path, syntax: mnu_idNN where id = NN
@app.route('/restaurants/menu_items/<string:mnu_id>/delete', methods=['GET', 'POST'])
def delete_menu_item_id(mnu_id):
    if request.method == 'GET':
        #get menu item id value
        mnu_id_val = int(mnu_id[6:])
        rest_menu_items = query_list_rest_menu_items_by_mnu(mnu_id_val)
        ftrd_rest_lst =[]
        for item in rest_menu_items:
            ftrd_rest_lst.append(query_restaurants(item['restaurant_id']))

        mnu_itm = query_menu_items(mnu_id_val)
        return render_template('delete_menu_item_id.html',  menu_item = mnu_itm,
                                rest_lst = ftrd_rest_lst)
        # return '3.2*. Returning form to delete menu item with id: ' + mnu_id[6:]
    
    if request.method == 'POST':
        if request.form.get('delete_button',0):
            #get menu item id value
            mnu_id_val = int(mnu_id[6:])
            # delete all records from RestMenuItem table
            idx = 0
            while idx < len(rest_menu_item_lst):
                if rest_menu_item_lst[idx]['menu_item_id'] == mnu_id_val:
                    # print('------\n', rest_menu_item_lst[idx])
                    rest_menu_item_lst.pop(idx)
                else:
                    idx += 1

            mnu_itm = query_menu_items(mnu_id_val)
            mnu_itm_idx = menu_item_lst.index(mnu_itm)
            menu_item_lst.pop(mnu_itm_idx)
            return redirect(url_for('menu_items'))
            # return '3.2*. Redirecting to page with menu items...

        if request.form.get('cancel_button',0):
            return redirect(url_for('menu_item_id', mnu_id = mnu_id ))
            # return '3.2*. Redirecting to page with menu item with id: ' + mnu_id[6:]


# 4*. Routing for list of all menu items
@app.route('/restaurants/menu_items/')
def menu_items():
    return render_template('menu_items.html', menu_items = menu_item_lst)
    # return '4*. Returning list of all menu items...  '


# 4.1*. Routing to add new menu item
@app.route('/restaurants/menu_items/add', methods=['GET', 'POST'])
def add_menu_item():
    # GET method - to send form
    if request.method == 'GET':
        return render_template('add_menu_item.html')
        # return '4.1*. Returning form to add new menu item... 

    # POST method - to recieve data and add to DB
    if request.method == 'POST':
        # add_button pressed - add to DB
        if request.form.get('add_button',0):
            new_menu_item = {'name' : request.form['name'], 
                             'description' : request.form['description'], 
                             'course' : request.form['course'], 
                             'weight' : int(request.form['weight']),
                             'content' : request.form['content'],
                             'id' : len(menu_item_lst) + 1}

            menu_item_lst.append(new_menu_item)
	        # new_menu_item = MenuItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], course = request.form['course'], restaurant_id = restaurant_id)
            # session.add(newItem)
	        # session.commit()
            return redirect(url_for('menu_items'))
            # return '4.1*. Redirecting to page with menu item...  

        # cancel_button pressed - redirect to menu items page
        if request.form.get('cancel_button',0):
            return redirect(url_for('menu_items'))
            # return '4.1*. Redirecting to page with menu item...     

# 5*. Routing to show 'News & Promo' page
@app.route('/restaurants/news_promo')
def news_promo():
    return '5*. Returning list of promo menu items... \
            (with not NULL comments at RestMenuItem table)  '

# 6*. Routing to show 'Contact us' page
@app.route('/restaurants/contact_us')
def contact_us():
    return '6*. Returning page with contacts info... '

        
# if mani module to execute
if __name__ == '__main__':
    # strat debug mode
    app.debug = True
    # run server at port 5000
    app.run(host='0.0.0.0', port=5000)




