import sqlite3

connection = sqlite3.connect('database.db')


with open('CryptoKeepCoding/schema.sql') as f:
    connection.executescript(f.read())
connection.close()