from tkinter import *
from tkinter import ttk

window = Tk()
window.title("Inventory Manager")

tabControl = ttk.Notebook(window)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

tabControl.add(tab1, text='Add Location')
tabControl.add(tab2, text='Add Inventory')
tabControl.pack(expand=1, fill='both')

ttk.Label(tab1, text='Enter new location name:').grid(column=0, row=0, padx=30, pady=30)
ttk.Label(tab2, text='Enter new item and quantity name:').grid(column=0, row=0, padx=30, pady=30)

window.mainloop()
