import tkinter
from tkinter import *
from tkinter import ttk

import sqlite3
from sqlite3 import OperationalError, IntegrityError

def add_store(*args):
    try:
        store_name = '_'.join(location_add.get().split())
        con.execute(f'''CREATE TABLE {store_name}
                          (NAME TEXT PRIMARY KEY NOT NULL,
                          QUANTITY INT NOT NULL);''')
        print('Table created successfully')
        create_display_menu(tab1, selected_loc).grid(column=0, row=0)
        create_display_menu(tab4, item_del).grid(column=2, row=0)
        create_display_menu(tab3, loc_add1).grid(column=2, row=0)
        create_display_menu(tab5, transfer_from).grid(column=1, row=3)
        create_display_menu(tab5, transfer_to).grid(column=1, row=4)
        return 1
    except OperationalError as e:
        print(e)
        if 'already exists' in str(e):
            print('Location already exists with given name.')
        else:
            print('Location name cannot start with a number or contain any special characters.')
        return 0


def add_items(name, quantity, store):
    # FIXME Finish add_items()
    # To be used with param (quantity, name, store)
    val = (name, quantity)
    try:
        con.execute(f"INSERT INTO {sql_strip(store)} (NAME, QUANTITY) VALUES (?, ?);", val)
    except OperationalError as e:
        if 'stores' in str(e):
            print("Please create a store using the 'Add Location' tab.")
        else:
            print('Please select a store.')
        return
    except IntegrityError as ie:
        print(f'Location {store} is empty.')

    print(f'{val[1]} {val[0]} added to {sql_strip(store)}')
    con.commit()
    return -1


def remove_items(name, quantity, store):
    """ 1st confirms that this item is in the store, then subtracts the specified amount from that item.
        If the specified amount to remove is greater that the stock, all stock is removed and a message
        is output declaring how much was removed."""
    try:
        cur = con.execute(f"SELECT quantity FROM {store} WHERE name == '{name}';")
        output = cur.fetchone()
        if output != None:
            if quantity > output[0]:
                print(f'{output[0]} {name} removed due to insufficient supply')
                con.execute(f"UPDATE {store} SET quantity={0} WHERE name='{name}'")
                con.commit()
                return output[0]
            else:
                print(f'{quantity} {name} removed from {store}')
                con.execute(f"UPDATE {store} SET quantity={output[0] - quantity} WHERE name='{name}'")
                con.commit()
                return quantity
        else:
            print('Item not found')
    except OperationalError as e:
        if 'created' in str(e):
            print('Please create a store to use this feature.')
        else:
            print('Please select a store')


def transfer(name, quantity, from_store, to_store):
    removed = remove_items(name, int(quantity), sql_strip(from_store))
    if removed is not None and int(removed) > 0:
        add_items(name, removed, sql_strip(to_store))
    return -1


def get_store_names():
    return con.execute("SELECT name FROM sqlite_master WHERE type='table';")


def get_store_items(store_name):
    cur = con.cursor()
    items = cur.execute(f"SELECT name, quantity FROM {store_name}")
    return items


# displays the inventory of each stores
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


# creates a dropdown menu that displays inventory of selected location
def create_display_menu(tab, drop_menu):
    nm = []
    for i in get_store_names():
        nm.append(i)
    if (len(nm) == 0):
        return OptionMenu(tab, drop_menu, 'No stores created')
    elif (drop_menu == selected_loc):
        return OptionMenu(tab, drop_menu, *nm,
                          command=display_store_information)
    else:
        return OptionMenu(tab, drop_menu, *nm)


def sql_strip(str):
    return str.strip('()\',')


window = Tk()
window.title("Inventory Manager")

con = sqlite3.connect('Inventory_Data.db')

# create and name tabs
tabControl = ttk.Notebook(window)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)
tab5 = ttk.Frame(tabControl)

tabControl.add(tab1, text='View Inventory')
tabControl.add(tab2, text='Add Location')
tabControl.add(tab3, text='Add Inventory')
tabControl.add(tab4, text='Remove Inventory')
tabControl.add(tab5, text='Transfer Inventory')
tabControl.pack(expand=1, fill='both')

# title tab1 and create a dropdown display menu that shows inventory at each location when called
ttk.Label(tab1, text='Inventory:')
selected_loc = StringVar()
create_display_menu(tab1, selected_loc).grid(column=0, row=0)

# adds new location from tab2 using add_store()
ttk.Label(tab2, text='Enter new location name:').grid(column=0, row=0, padx=15, pady=15)
location_add = StringVar()
location_entry = ttk.Entry(tab2, width=15, textvariable=location_add).grid(column=1, row=1, padx=15, pady=15)
ttk.Button(tab2, text="Add", command=lambda: add_store(location_add.get())).grid(column=2, row=2, padx=15, pady=15)

# adds new items etc from tab3 using add_items()
ttk.Label(tab3, text='Enter name of new item and quantity:').grid(column=0, row=0, padx=15, pady=8)
ttk.Label(tab3, text='Item name:').grid(column=0, row=1, padx=15, pady=5)
ttk.Label(tab3, text='Quantity:').grid(column=1, row=1, padx=15, pady=5)
item_add = StringVar()
item_entry = ttk.Entry(tab3, width=15, textvariable=item_add).grid(column=0, row=2, padx=15, pady=15)
quantity_add = StringVar()
quantity_entry = ttk.Entry(tab3, width=15, textvariable=quantity_add).grid(column=1, row=2, padx=15, pady=15)
loc_add1 = StringVar()
create_display_menu(tab3, loc_add1).grid(column=2, row=0)
ttk.Button(tab3, text="Add", command=lambda: add_items(item_add.get(), quantity_add.get(), loc_add1.get())).grid(
    column=2, row=2, padx=15, pady=15)

# removes items
ttk.Label(tab4, text='Enter Name of Item to be Deleted:').grid(column=0, row=0, padx=15, pady=8)
ttk.Label(tab4, text='Item name').grid(column=0, row=1, padx=15, pady=5)
ttk.Label(tab4, text='Quantity:').grid(column=1, row=1, padx=15, pady=5)
remove_item = StringVar()
remove_itemname = ttk.Entry(tab4, width=15, textvariable=remove_item).grid(column=0, row=2, padx=15, pady=15)
quantity_remove = StringVar()
quantity_entry = ttk.Entry(tab4, width=15, textvariable=quantity_remove).grid(column=1, row=2, padx=15, pady=15)
item_del = StringVar()
create_display_menu(tab4, item_del).grid(column=2, row=0)
ttk.Button(tab4, text="Remove Items",
           command=lambda: remove_items(remove_item.get(), int(quantity_remove.get()), sql_strip(item_del.get()))).grid(
    column=2, row=2,
    padx=15, pady=15)

# transfers items
ttk.Label(tab5, text='Enter name of item and quantity to be transfered.').grid(column=0, row=0, padx=8, pady=8)
ttk.Label(tab5, text='Item name:').grid(column=0, row=1, padx=15, pady=5)
name_transfer = StringVar()
name_entry = ttk.Entry(tab5, width=15, textvariable=name_transfer).grid(column=1, row=1, padx=15, pady=5)
ttk.Label(tab5, text='Quantity:').grid(column=0, row=2, padx=15, pady=5)
quantity_tranfer = StringVar()
quantity_entry = ttk.Entry(tab5, width=15, textvariable=quantity_tranfer).grid(column=1, row=2, padx=15, pady=5)
ttk.Label(tab5, text='From:').grid(column=0, row=3, padx=15, pady=5)
transfer_from = StringVar()
create_display_menu(tab5, transfer_from).grid(column=1, row=3)
ttk.Label(tab5, text='To:').grid(column=0, row=4, padx=15, pady=5)
transfer_to = StringVar()
create_display_menu(tab5, transfer_to).grid(column=1, row=4)
ttk.Button(tab5, text='Transfer',
           command=lambda: transfer(name_transfer.get(), quantity_tranfer.get(), transfer_from.get(),
                                    transfer_to.get())).grid(column=2, row=4, padx=15, pady=5)

# runs main loop
window.mainloop()
