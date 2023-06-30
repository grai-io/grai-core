from .base import BaseAdapter


class MySQLAdapter(BaseAdapter):
    def get_integration(self):
        from grai_source_mysql.base import MysqlIntegration

        metadata = self.run.connection.metadata
        secrets = self.run.connection.secrets

        return MysqlIntegration(
            source={
                "id": self.run.source.id,
                "name": self.run.source.name,
            },
            host=metadata["host"],
            port=metadata["port"],
            dbname=metadata["dbname"],
            user=metadata["user"],
            password=secrets["password"],
            namespace=self.run.connection.namespace,
        )
