import psycopg2
import psycopg2.extras


def get_connection(dbname, user, password, host='localhost'):
    connect_str = f"dbname={dbname} host='{host}' user='{user}' password='{password}'"
    return psycopg2.connect(connect_str)


def query_runner(query, param_dict={}):
    with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        cursor.execute(query, param_dict)
        result = cursor.fetchall()
    return result


def get_tables(connection: psycopg2.connect):
    """
    Create and return a list of dictionaries with the
    schemas and names of tables in the database
    connected to by the connection argument.
    """

    query = """
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_schema != 'pg_catalog'
        AND table_schema != 'information_schema'
        AND table_type='BASE TABLE'
        ORDER BY table_schema, table_name
    """
    return query_runner(query)


def get_columns(connection, table_schema, table_name):
    """
    Creates and returns a list of dictionaries for the specified
    schema.table in the database connected to.
    """

    query = """
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_schema = %(table_schema)s
        AND table_name   = %(table_name)s
        ORDER BY ordinal_position
    """

    where_dict = {"table_schema": table_schema, "table_name": table_name}

    return query_runner(query, where_dict)


def get_foreign_keys(connection):
    """This needs to be tested / evaluated
    :param connection:
    :return:
    """
    query = """
         SELECT conrelid::regclass AS table_name, 
               conname AS foreign_key, 
               pg_get_constraintdef(oid) 
        FROM   pg_constraint 
        WHERE  contype = 'f' 
        AND    connamespace = 'public'::regnamespace   
        ORDER  BY conrelid::regclass::text, contype DESC;
    """

    return query_runner(query)


def get_tree(connection):
    """
    Uses get_tables and get_columns to create a tree-like data
    structure of tables and columns.
    It is not a true tree but a list of dictionaries containing
    tables, each dictionary having a second dictionary
    containing column information.
    """

    tree = get_tables(connection)

    for table in tree:
        table["columns"] = get_columns(connection, table["table_schema"], table["table_name"])

    return tree


def print_tree(tree):
    """
    Prints the tree created by get_tree
    """
    for table in tree:
        print(f'{table["table_schema"]}.{table["table_name"]}')
        for column in table["columns"]:
            print(f'|-{column["column_name"]} ({column["data_type"]})')
    print(dict(column))


if __name__ == '__main__':
    connection = get_connection('docker', 'docker', 'docker')
    res = get_tree(connection)
    print_tree(res)

    fk = get_foreign_keys(connection)
    print(fk)