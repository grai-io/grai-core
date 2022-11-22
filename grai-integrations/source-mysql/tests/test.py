import mysql.connector as cnx

connection_args = {
    'host': 'localhost',
    'database': 'db',
    'user': 'docker',
    'password': 'docker'
}

param_dict = {
  'use_pure': True
}

mydb = cnx.connect(**connection_args)

#mydb = mysql.connector.connect(
#  host="localhost",
#  user="docker", 
#  password="docker",
#  database="db"
#)

mycursor = mydb.cursor(dictionary=True)

mycursor.execute("""SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_schema != 'information_schema'
		    AND table_schema != 'performance_schema'
            ORDER BY table_schema, table_name""")

myresult = mycursor.fetchall()


for x in myresult:
  print(x)

print(type(myresult))


def build_dict(cursor, row):
    x = {}
    for key,col in enumerate(cursor.description):
        x[col[0]] = row[key]
    return d

build_dict(myresult)

fruits = ["Apple", "Pear", "Peach", "Banana"]

fruit_dictionary = { fruit : "In stock" for fruit in fruits }

print(fruit_dictionary)

print(type(fruit_dictionary))