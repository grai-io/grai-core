import uuid


class Node:
    def __init__(self):
        self.node_id = uuid.uuid4()
        # self.ancestor_id = ancestor_id
        # self.updated_at = update_time


class DataElement(Node):
    pass


class DataCollection:
    pass


class DataColumn(DataCollection):
    pass


class TableData(DataCollection):
    pass


class APIData(Node):
    pass
