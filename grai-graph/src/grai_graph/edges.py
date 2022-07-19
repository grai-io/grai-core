import uuid


class Edge:
    def __init__(self):
        self.id = uuid.uuid4()

        # self.updated_at = update_time


class SQLTransformation(Edge):
    def __init__(self, sql_code):
        self.code = sql_code
