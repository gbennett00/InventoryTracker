import tkinter
from tkinter import *
from tkinter import ttk

import sqlite3


def add_store(*args):
    try:
        store_name = '_'.join(location_add.get().split())
        con.execute(f'''CREATE TABLE {store_name}
                          (NAME TEXT PRIMARYY KEY NOT NULL,
                          QUANTITY INT NOT NULL);''')
        print('Table created successfully')
        return 1
    except:
        print('Location already exists')
        return 0


def add_items(*args):
    # FIXME Finish add_items()
    # To be used with param (quantity, name)
    '''from sqlite3 import Error
      def sql_connection:
        try:
          conn = sqlite3.connect(#insertdatabase name)
          return conn
        except Error:
          print(Error)
      def sql_table(conn):
        cursorObj = conn.cursor()
        cursorObj.execute("Store inventory")
          print('Item added successfully')'''
    return -1


def lost_items(*args):
    # FIXME Finish lost_items()
    # To be used with param (quantity, name)
    return -1


def transfer():
    # FIXME Finish transfer()
    return -1

def get_store_names():
    return con.execute("SELECT name FROM sqlite_master WHERE type='table';")

def display_store_items():
    # FIXME Finish display_store_items
    return -1


window = Tk()
window.title("Inventory Manager")

con = sqlite3.connect('Inventory_Data.db')

tabControl = ttk.Notebook(window)
#create and name tabs
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)

tabControl.add(tab1, text='View Inventory')
tabControl.add(tab2, text='Add Location')
tabControl.add(tab3, text='Add Inventory')
tabControl.pack(expand=1, fill='both')

#format and fill tabs
ttk.Label(tab1, text='Inventory:')
ttk.Label(tab2, text='Enter new location name:').grid(column=0, row=0, padx=15, pady=15)
ttk.Label(tab3, text='Enter name of new item and quantity:').grid(column=0, row=0, padx=15, pady=15)

#displays table information
selected_loc = StringVar()
display_menu = OptionMenu(tab1, selected_loc, 'Select store:', *get_store_names())
display_menu.pack()

#adds new location from tab2 using add_store()
location_add = StringVar()
location_entry = ttk.Entry(tab2, width=15, textvariable=location_add).grid(column=1, row=1, padx=15, pady=15)
ttk.Button(tab2, text="Add", command=add_store).grid(column=2, row=2, padx=15, pady=15)

#adds new items etc from tab3 using add_items()
item_add = StringVar()
item_entry = ttk.Entry(tab3, width=15, textvariable=item_add).grid(column=1, row=1, padx=15, pady=15)
ttk.Button(tab3, text="Add", command=add_items).grid(column=2, row=2, padx=15, pady=15)

window.mainloop()
