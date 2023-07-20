from .graph import GraphQuery


def filter_by_filter(filter, query: GraphQuery) -> GraphQuery:
    if len(filter.metadata) == 0:
        return query

    for row in filter.metadata:
        value = row["value"]

        if row["type"] == "table":
            if row["field"] == "name":
                if row["operator"] == "equals":
                    query.where(f"toLower(table.name) = toLower('{value}')")
                elif row["operator"] == "not-equals":
                    query.where(f"toLower(table.name) <> toLower('{value}')")
                elif row["operator"] == "contains":
                    query.where(f"toLower(table.name) CONTAINS toLower('{value}')")
                elif row["operator"] == "not-contains":
                    query.where(f"NOT toLower(table.name) CONTAINS toLower('{value}')")
                elif row["operator"] == "starts-with":
                    query.where(f"toLower(table.name) STARTS WITH toLower('{value}')")
                elif row["operator"] == "ends-with":
                    query.where(f"toLower(table.name) ENDS WITH toLower('{value}')")

            elif row["field"] == "tag":
                if row["operator"] == "contains":
                    query.where(f"'{value}' IN table.tags")
        elif row["type"] == "ancestor":
            if row["field"] == "tag":
                if row["operator"] == "contains":
                    query.match(
                        "(table)<-[:TABLE_TO_TABLE|:TABLE_TO_TABLE_COPY*]-(othertable:Table)",
                        where=f"'{value}' IN othertable.tags",
                    )
        elif row["type"] == "no-ancestor":
            if row["field"] == "tag":
                if row["operator"] == "contains":
                    # where.append(f"(table)<-[:TABLE_TO_TABLE|:TABLE_TO_TABLE_COPY*]-(othertable:Table) AND '{value}' IN othertable.tags")
                    pass
        elif row["type"] == "descendant":
            if row["field"] == "tag":
                if row["operator"] == "contains":
                    query.match(
                        "(table)-[:TABLE_TO_TABLE|:TABLE_TO_TABLE_COPY*]->(othertable:Table)",
                        where=f"'{value}' IN othertable.tags",
                    )
        elif row["type"] == "no-descendant":
            if row["field"] == "tag":
                if row["operator"] == "contains":
                    # where.append(f"(table)-[:TABLE_TO_TABLE|:TABLE_TO_TABLE_COPY*]->(othertable:Table) AND '{value}' IN othertable.tags")
                    pass
        else:
            raise Exception("Unknown filter type: " + row["type"])

    return query
