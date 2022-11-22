import psycopg2
import psycopg2.extras

connection_args = {
    'host': 'localhost',
    'database': 'docker',
    'user': 'docker',
    'password': 'docker',
    'port': '5432'
}

mydb = psycopg2.connect(**connection_args)

#mydb = mysql.connector.connect(
#  host="localhost",
#  user="docker", 
#  password="docker",
#  database="db"
#)

mycursor = mydb.cursor()

query = ("""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_schema != 'pg_catalog'
            AND table_schema != 'information_schema'
            AND table_type='BASE TABLE'
            ORDER BY table_schema, table_name
            """)

with mydb.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        ) as cursor:
            cursor.execute(query)
            myresult = cursor.fetchall()


for x in myresult:
  print(x)

print(type(myresult))

fruits = ["Apple", "Pear", "Peach", "Banana"]

fruit_dictionary = { fruit : "In stock" for fruit in fruits }

print(fruit_dictionary)

print(type(fruit_dictionary))