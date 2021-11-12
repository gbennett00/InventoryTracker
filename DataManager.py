import sqlite3

con = sqlite3.connect('DataBase1')
print('Database successfully connected')
con.close()