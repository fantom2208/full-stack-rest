# reading data from tables restaurant db

# Connection to DB and adding information in tables via script
# create_engine will point (connect) to database we used 
from sqlalchemy import create_engine
# import to make connection to 
from sqlalchemy.orm import sessionmaker
##import filtering for query objects
##from sqlalchemy_filters import apply_filters
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


# ----- handling logic for reading db ----- 
# function to get dictioary of class attributes (table columns)
def get_attr_dict(cls_obj):
    elm = vars(cls_obj)
    idx = 1
    columns = {}
    # loop for all keys (properties)
    for item in elm:
        columns[idx] = item
        idx += 1
    return columns


# function to print dictionary content (columns)
def print_dict(dict):
    for (key, val) in dict.items():
        print(' ', key, '-', val)

# function to print list of record for specific column
def print_tbl_clmn(tbl_rec, cln_name = ''):
    print(' ')
    print('id  name        ', cln_name)
    for item in tbl_rec:
        # get id 
        id = item.id
        # get name 
        try: 
            name = item.name
        except:
            name = ""
        # get column value if needed
        if cln_name:
            val = getattr(item, cln_name)
        else:
            val = ''
        print (id, '  ', name,  ' -- ', val)
##    print(' ')

# function to set new column value
def set_tbl_clmn(tbl_rec, cln_name, new_val):
    for item in tbl_rec:
        # set new column value 
        setattr(item, cln_name, new_val)

# function to select records acc to filter criteria
def apply_filter(items, filter):
    filter_splt = filter.split(' ')
    clmn = filter_splt[0]
    op = filter_splt[1]
    vle = ' '.join(filter_splt[2:])

    #check if value string or not
    ite_val = getattr(items[0], clmn)
    if not isinstance(ite_val, str):
        vle = eval(vle)

    ##print(filter_splt)
    ##print(clmn)
    ##print(op)
    ##print(vle)

    filter_lst = []
    for item in items:
        ite_val = getattr(item, clmn)
        # if '=' operator and values are equal, then to add
        if op == '=' or op == '==':
            if ite_val == vle:
                filter_lst.append(item)

        # if '!=' operator and values are not equal, then to add
        if op == '!=' or op == '<>':
            if ite_val != vle:
                filter_lst.append(item)        

        # if '>' operator and values are >, then to add
        if op == '>':
            if ite_val > vle:
                filter_lst.append(item) 
        
        # if '<' operator and values are <, then to add
        if op == '<':
            if ite_val < vle:
                filter_lst.append(item) 
    # return riltered list
    return filter_lst


# define table dictionary
tbl_dict = {1 : Restaurant,
            2 : MenuItem,
            3 : RestMenuItem}

# main script logic
def delete_db_rec(rest_ses):
    # flag for table and table select loop
    tbl_flag = 1
    while tbl_flag:
        print('Select item(table) number: \n  0 - exit to shell')
        print_dict(tbl_dict)
        try:
            tbl_flag = eval(input())
        except:
            print('Please, enter number from list above')
            continue    # while tbl_flag:

        # if not (0 - exit), then select table name from dict
        if tbl_flag:
            tbl_name = tbl_dict.get(tbl_flag, 0)
            
            # if table found in dictioary, thaen select all records
            if not tbl_name:
                #no class found in dictionary
                print('Please, enter correct number from list above')
                continue    # while tbl_flag:
            
            # else:
            #get all table record (to define columns)
            all_rec = rest_ses.query(tbl_name).all()  
                
            # if not empty table - define column dictionary by first element
            if not len(all_rec):    #check return result for  empty table!
                print('Table is empty, select another one')
                continue    # while tbl_flag:
            
            # else:
            # get attribut dictioanary
            cln_dic = get_attr_dict(all_rec[0])
            print('List of table columns:')
            print_dict(cln_dic)

            # flag for filter select loop
            fltr_flag = '*'
            #get all table record to initial filter list
            fltr_rec = all_rec.copy() 
            while fltr_flag != '!*':
                print("Enter a query filter: \n  !* - to exit to table list")
                print('  or * to select all records\n  or like: column_name op value\n  where op could be =, >, <, !=')

                # input filter criteria
                fltr_flag = input('Filter: ')
                if fltr_flag == '!*':
                    continue    #while fltr_flag:

                if fltr_flag == '*':
                    #get all table record (to define co;lumns)
                    fltr_rec = all_rec.copy()
                else:
                    # try to apply filter in query
                    try:
                        # apply filter via function
                        fltr_rec = apply_filter(fltr_rec, fltr_flag)
                                            
                        # manual input
                        ## fltr_rec = rest_ses.query(tbl_name).filter_by(name = 'Veggie Burger').all()
                    except:
                        print('Filter sintax mistake, try anoter one.')
                        continue    #while fltr_flag:
                        
                ##print_tbl_clmn(fltr_rec)
                ##print(type(fltr_rec))

                if not len(fltr_rec): #check return result for empty table!
                    # if empty responce table
                    print('Responce table is empty, try anoter filter.')
                    continue    #while fltr_flag:
                        
                # else:
                # print esponce table (id and name)
                print('It was selected following set of records:')
                print_tbl_clmn(fltr_rec)

                # confirm continue update process
                contn = input("\nTo continue delete process enter 'y':")
                if contn.lower() != 'y':
                    print('Returning to enter filter criteria ...')
                    continue    #while fltr_flag:
                            
                # else:
                # flag for table select and table select loop
                cln_flag = 1
                while cln_flag:
                    print('Select item(column) number to check before delete: \n  0 - exit to table list')
                    print_dict(cln_dic)

                    try:
                        cln_flag = eval(input())
                    except:
                        print('Please, enter number from list above') 
                        continue    # while cln_flag:                 
                        
                    # if not (0 - go to tables), then select column name from dict
                    if cln_flag:
                        # select column name from dictionary
                        cln_name = cln_dic.get(cln_flag, 0)
                            
                        if not cln_name:
                            # if column found in dictioary, thaen select all records
                            print('Please, enter correct number from list above') 
                            continue    # while cln_flag:  
                        #else:
                        print('Selected records to delete:', cln_name)
                        print_tbl_clmn(fltr_rec, cln_name)

                        # confirm continue delete process
                        contn = input("\nTo commit delete enter 'y':")
                        if contn.lower() != 'y':
                            print('Returning to enter column to view ...')
                            continue    #while cln_flag:
                        
                        # loop to stage 
                        for item in fltr_rec:
                            # delete item
                            rest_ses.delete(item)
                        #commit changes
                        rest_ses.commit()
                        print('\nApply filter again to check updated values in database.\nReturning to table select menu...\n')
                        cln_flag = 0        # clear cln_flag to exit loop
                        fltr_flag = '!*'    # clear fltr_flag to exit loop


# if mani module to execute
if __name__ == '__main__':
    # set connections
    rest_ses = set_connection()
    # read db CLI
    delete_db_rec(rest_ses)                    