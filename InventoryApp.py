import tkinter
from tkinter import Tk, StringVar, OptionMenu
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
        print('Unable to create table (likely because table already exists)')
        return 0


def add_items(name, quantity, store):
    # FIXME Finish add_items()
    # To be used with param (quantity, name, store)
    val = (name, quantity)
    con.execute(f"INSERT INTO {store} (NAME, QUANTITY) VALUES (?, ?);", val)
    print(f'{val[1]} {val[0]} added to database')
    con.commit()
    return -1


def remove_items(*args):
    # FIXME Finish remove_items()
    # To be used with param (quantity, name)
    return -1


def transfer():
    # FIXME Finish transfer()
    return -1

def get_store_names():
    return con.execute("SELECT name FROM sqlite_master WHERE type='table';")

def get_store_items(store_name):
    cur = con.cursor()
    items = cur.execute(f"SELECT name, quantity FROM {store_name}")
    return items

# displays the inventory of
def display_store_information(*args):
  columns = ('Name', 'Quantity')
  tree = ttk.Treeview(tab1, columns=columns, show='headings')
  tree.grid(row=1, column=0)

  for col in columns:
      tree.heading(col, text=col)
      tree.column(col, width=100, anchor=tkinter.CENTER)

  for rec in sorted(get_store_items(selected_loc.get().strip('()\','))):
      tree.insert('', 'end', value=rec)

  sb = tkinter.Scrollbar(tab1, orient=tkinter.VERTICAL, command=tree.yview)
  sb.grid(row=1, column=1, sticky='ns')
  return 1

#creates a dropdown menu that displays inventory of selected location
def create_display_menu(tab, drop_menu):
    nm = []
    for i in get_store_names():
        nm.append(i)
    if(len(nm) == 0):
        return OptionMenu(tab, drop_menu, 'No stores created')
    elif(drop_menu == selected_loc):
        return OptionMenu(tab, drop_menu, *nm,
                          command=display_store_information)
    else:
        return OptionMenu(tab, drop_menu, *nm)

window = Tk()
window.title("Inventory Manager")

con = sqlite3.connect('Inventory_Data.db')

#create and name tabs
tabControl = ttk.Notebook(window)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)

tabControl.add(tab1, text='View Inventory')
tabControl.add(tab2, text='Add Location')
tabControl.add(tab3, text='Add Inventory')
tabControl.pack(expand=1, fill='both')


#title tab1 and create a dropdown display menu that shows inventory at each location when called
ttk.Label(tab1, text='Inventory:')
selected_loc = StringVar()
display_menu = create_display_menu(tab1, selected_loc)
display_menu.grid(column=0, row=0)


#adds new location from tab2 using add_store()
ttk.Label(tab2, text='Enter new location name:').grid(column=0, row=0, padx=15, pady=15)
location_add = StringVar()
location_entry = ttk.Entry(tab2, width=15, textvariable=location_add).grid(column=1, row=1, padx=15, pady=15)
ttk.Button(tab2, text="Add", command=lambda: add_store(location_add.get())).grid(column=2, row=2, padx=15, pady=15)


#adds new items etc from tab3 using add_items()
ttk.Label(tab3, text='Enter name of new item and quantity:').grid(column=0, row=0, padx=15, pady=15)
item_add = StringVar()
item_entry = ttk.Entry(tab3, width=15, textvariable=item_add).grid(column=1, row=1, padx=15, pady=15)
loc_add1 = StringVar()
loc_tab2 = create_display_menu(tab2, loc_add1)
loc_tab2.grid(column=2, row=0)

ttk.Button(tab3, text="Add", command=add_items).grid(column=2, row=2, padx=15, pady=15)

#runs main loop
window.mainloop()
