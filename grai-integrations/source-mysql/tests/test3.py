import psycopg2
import psycopg2.extras
import json


def query_runner(query):
    with mydb.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor
    ) as cursor:
        cursor.execute(query, param_dict)
        result = cursor.fetchall()
    return [dict(item) for item in result]

connection_args = {
    'host': 'localhost',
    'database': 'docker',
    'user': 'docker',
    'password': 'docker',
    'port': '5432'
}

param_dict = {
  'use_pure': True
}

mydb = psycopg2.connect(**connection_args)

mycursor = mydb.cursor()

query = ("""
            SELECT c.conname                                         AS constraint_name,
                   c.contype                                         AS constraint_type,
                   sch.nspname                                       AS "self_schema",
                   tbl.relname                                       AS "self_table",
                   ARRAY_AGG(col.attname ORDER BY u.attposition)     AS "self_columns",
                   f_sch.nspname                                     AS "foreign_schema",
                   f_tbl.relname                                     AS "foreign_table",
                   ARRAY_AGG(f_col.attname ORDER BY f_u.attposition) AS "foreign_columns",
                   pg_get_constraintdef(c.oid)                       AS definition
            FROM pg_constraint c
                   LEFT JOIN LATERAL UNNEST(c.conkey) WITH ORDINALITY AS u(attnum, attposition) ON TRUE
                   LEFT JOIN LATERAL UNNEST(c.confkey) WITH ORDINALITY AS f_u(attnum, attposition) ON f_u.attposition = u.attposition
                   JOIN pg_class tbl ON tbl.oid = c.conrelid
                   JOIN pg_namespace sch ON sch.oid = tbl.relnamespace
                   LEFT JOIN pg_attribute col ON (col.attrelid = tbl.oid AND col.attnum = u.attnum)
                   LEFT JOIN pg_class f_tbl ON f_tbl.oid = c.confrelid
                   LEFT JOIN pg_namespace f_sch ON f_sch.oid = f_tbl.relnamespace
                   LEFT JOIN pg_attribute f_col ON (f_col.attrelid = f_tbl.oid AND f_col.attnum = f_u.attnum)
            GROUP BY constraint_name, constraint_type, "self_schema", "self_table", definition, "foreign_schema", "foreign_table"
            ORDER BY "self_schema", "self_table"
            """)

result = query_runner(query)

mycursor.execute("""
            SELECT c.conname                                         AS constraint_name,
                   c.contype                                         AS constraint_type,
                   sch.nspname                                       AS "self_schema",
                   tbl.relname                                       AS "self_table",
                   ARRAY_AGG(col.attname ORDER BY u.attposition)     AS "self_columns",
                   f_sch.nspname                                     AS "foreign_schema",
                   f_tbl.relname                                     AS "foreign_table",
                   ARRAY_AGG(f_col.attname ORDER BY f_u.attposition) AS "foreign_columns",
                   pg_get_constraintdef(c.oid)                       AS definition
            FROM pg_constraint c
                   LEFT JOIN LATERAL UNNEST(c.conkey) WITH ORDINALITY AS u(attnum, attposition) ON TRUE
                   LEFT JOIN LATERAL UNNEST(c.confkey) WITH ORDINALITY AS f_u(attnum, attposition) ON f_u.attposition = u.attposition
                   JOIN pg_class tbl ON tbl.oid = c.conrelid
                   JOIN pg_namespace sch ON sch.oid = tbl.relnamespace
                   LEFT JOIN pg_attribute col ON (col.attrelid = tbl.oid AND col.attnum = u.attnum)
                   LEFT JOIN pg_class f_tbl ON f_tbl.oid = c.confrelid
                   LEFT JOIN pg_namespace f_sch ON f_sch.oid = f_tbl.relnamespace
                   LEFT JOIN pg_attribute f_col ON (f_col.attrelid = f_tbl.oid AND f_col.attnum = f_u.attnum)
            GROUP BY constraint_name, constraint_type, "self_schema", "self_table", definition, "foreign_schema", "foreign_table"
            ORDER BY "self_schema", "self_table"
            """)

myresult = mycursor.fetchall()

for i in result:
  print(type(i))
  print((i))
  print((i.keys()))
  print((i.items()))
  print(i["self_columns"])
  print(type(i["self_columns"]))

