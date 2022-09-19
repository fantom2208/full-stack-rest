# reading data from tables restaurant db

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
    print(' ')


# define table dictionary
tbl_dict = {1 : Restaurant,
            2 : MenuItem,
            3 : RestMenuItem}


# main script logic
def read_db_rec(rest_ses):
    # flag for table select and table select loop
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
            #get all table records
            all_rec = rest_ses.query(tbl_name).all()   
                
            # if not empty table - define column dictionary by first element
            if not len(all_rec): #check return result for  empty table!
                print('Table is empty, select another one')
                continue    # while tbl_flag:
            
            # else:
            # get attribut dictioanary
            cln_dic = get_attr_dict(all_rec[0])

            # flag for column and column select loop
            cln_flag = 1
            while cln_flag:
                print('Select item(column) number: \n  0 - exit to table list')
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
                    
                    # else:
                    # print table with column content
                    print_tbl_clmn(all_rec, cln_name)



# if mani module to execute
if __name__ == '__main__':
    # set connections
    rest_ses = set_connection()
    # read db CLI
    read_db_rec(rest_ses)
