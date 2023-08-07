from .graph import GraphQuery


def filter_by_filter(filter, query: GraphQuery) -> GraphQuery:
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

            elif row["field"] == "namespace":
                if row["operator"] == "equals":
                    query.where(f"table.namespace = '{value}'")
                elif row["operator"] == "in":
                    list = "['" + "', '".join(value) + "']"
                    query.where(f"table.namespace IN {list}")

            elif row["field"] == "data-source":
                if row["operator"] == "in":
                    list = "['" + "', '".join(value) + "']"
                    query.where(f"any(x IN table.data_sources WHERE x IN {list})")

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
                    query.optional_match(
                        "(table)<-[:TABLE_TO_TABLE|:TABLE_TO_TABLE_COPY*]-(othertable:Table)"
                    ).withWhere(
                        f"WHERE (othertable is null or not '{value}' IN othertable.tags)"
                    )
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
                    query.optional_match(
                        "(table)-[:TABLE_TO_TABLE|:TABLE_TO_TABLE_COPY*]->(othertable:Table)"
                    ).withWhere(
                        f"WHERE (othertable is null or not '{value}' IN othertable.tags)"
                    )
        else:
            raise Exception("Unknown filter type: " + row["type"])

    return query
