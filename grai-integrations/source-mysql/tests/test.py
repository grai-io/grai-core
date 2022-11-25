import mysql.connector as cnx
import json


def query_runner(query):
  dict_cursor = mydb.cursor(dictionary=True)
  dict_cursor.execute(query)
  result = dict_cursor.fetchall()
  for item in result:
    for x in item:
      x.lower()
  for item in result:
    dict(item)
  return result

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

mycursor = mydb.cursor(dictionary=True)

query = ("""select
            tc.CONSTRAINT_NAME as constraint_name,
            case when tc.CONSTRAINT_TYPE='PRIMARY KEY' then 'p'
                when tc.CONSTRAINT_TYPE='FOREIGN KEY' then 'f' end as constraint_type,
            'public' as self_schema,
            tc.TABLE_NAME as self_table, 
            GROUP_CONCAT(kcu.COLUMN_NAME SEPARATOR ',') self_columns,
            JSON_ARRAYAGG(kcu.COLUMN_NAME) self_columns2,
            'public' as foreign_schema,
            kcu.REFERENCED_TABLE_NAME as foreign_table,
            GROUP_CONCAT(kcu.REFERENCED_COLUMN_NAME SEPARATOR ',') as foreign_columns,
            JSON_ARRAYAGG(kcu.REFERENCED_COLUMN_NAME) as foreign_columns2,
            CONCAT(tc.CONSTRAINT_TYPE, ' (', GROUP_CONCAT(kcu.COLUMN_NAME), ')', (case when tc.CONSTRAINT_TYPE = 'FOREIGN KEY' then CONCAT(' REFERENCES ',kcu.REFERENCED_TABLE_NAME,'(',GROUP_CONCAT(kcu.REFERENCED_COLUMN_NAME),')') else '' end) ) as definition
        from
            information_schema.TABLE_CONSTRAINTS tc 
        join information_schema.KEY_COLUMN_USAGE kcu on 
            (kcu.TABLE_SCHEMA = tc.TABLE_SCHEMA 
            or kcu.REFERENCED_TABLE_SCHEMA = tc.TABLE_SCHEMA) 
            and (kcu.TABLE_NAME = tc.TABLE_NAME 
            or kcu.REFERENCED_TABLE_NAME = tc.TABLE_NAME)
            and kcu.CONSTRAINT_NAME = tc.CONSTRAINT_NAME  
        group by 
            tc.CONSTRAINT_NAME,
            tc.CONSTRAINT_TYPE,
            tc.TABLE_NAME,
            kcu.REFERENCED_TABLE_NAME""")

result = query_runner(query)

'''
for i in result:
  #print(type(i))
  #print((i))
  print((i.keys()))
  print((i.items()))
  (i["self_columns"]) = list(i["self_columns"].values())
  print(type(i["self_columns"]))
  print(i["self_columns"])
  print(type(i["self_columns2"]))
  print(i["self_columns2"])
  #json.loads(i["self_columns"])
'''


#str_1 = "then, we, go"
#list_1 = str_1.split(',')
#print(list_1)
#print(type(list_1))
#print(str_1)
#print(type(str_1))


for i in result:
  #print(i)
  #i["self_columns"] = list(i["self_columns"])
  #print(type(i["self_columns"]))
  #print(i["self_columns"])

  i["self_columns"] = list(i["self_columns"].split(","))
  print(type(i["self_columns"]))
  print(i["self_columns"])