import MySQLdb

host = 'oniddb.cws.oregonstate.edu'
name = 'rymalc-db'
user = 'rymalc-db'
passwd = 'HIJGYGHHGCWXieGl'

"""
db = MySQLdb.connect(host="localhost", # your host, usually localhost
		user="john", # your username
		passwd="megajonhy", # your password
		db="jonhydb") # name of the data base
"""

db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=name)


# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor() 

# Use all the SQL you like
cur.execute("SELECT * FROM db0_pub")

# print all the first cell of all the rows
for row in cur.fetchall():
	print row[0]

