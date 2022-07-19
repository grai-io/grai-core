from grai_source_postgres.loader import PostgresConnector


def get_nodes_and_edges(dbname: str, user: str, password: str, host: str = 'localhost', port: str = '5432'):
    connector = PostgresConnector(dbname, user, password, host, port)
    with connector.connect() as conn:
        nodes = conn.get_nodes()
        fks = conn.get_foreign_keys()
    return nodes, fks
