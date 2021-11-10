from tkinter import *
from tkinter import ttk

window = Tk()
window.title("Create Database")

mainframe = ttk.Frame(window, padding="3 3 15 15")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

name = StringVar()
name_entry = ttk.Entry(mainframe, width=7, textvariable=name)
name_entry.grid(column=2, row=1, sticky=(N, W))

meters = StringVar()
ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(N, W))



window.mainloop()