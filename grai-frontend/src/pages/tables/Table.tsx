import React from "react"
import { gql, useQuery } from "@apollo/client"
import { useParams } from "react-router-dom"
import NotFound from "pages/NotFound"
import TableHeader from "components/tables/TableHeader"
import TableContent from "components/tables/TableContent"
import GraphError from "components/utils/GraphError"
import PageLayout from "components/layout/PageLayout"
import { GetTable, GetTableVariables } from "./__generated__/GetTable"
import { tableToEnhancedTable } from "helpers/graph"

export const GET_TABLE = gql`
  query GetTable($workspaceId: ID!, $tableId: ID!) {
    workspace(pk: $workspaceId) {
      id
      table(pk: $tableId) {
        id
        namespace
        name
        display_name
        is_active
        data_source
        metadata
        columns {
          id
          name
          display_name
        }
      }
      tables {
        id
        namespace
        name
        display_name
        data_source
        metadata
        columns {
          id
          name
          display_name
        }
      }
      other_edges {
        id
        source {
          id
        }
        destination {
          id
        }
        metadata
      }
    }
  }
`

const Table: React.FC = () => {
  const { workspaceId, tableId } = useParams()

  const { loading, error, data } = useQuery<GetTable, GetTableVariables>(
    GET_TABLE,
    {
      variables: {
        workspaceId: workspaceId ?? "",
        tableId: tableId ?? "",
      },
    }
  )

  if (error) return <GraphError error={error} />
  if (loading) return <PageLayout loading />

  const table = data?.workspace?.table

  if (!table) return <NotFound />

  const enhancedTable = tableToEnhancedTable(
    table,
    data.workspace.tables,
    data.workspace.other_edges
  )

  return (
    <PageLayout>
      <TableHeader table={table} />
      <TableContent table={enhancedTable} />
    </PageLayout>
  )
}

export default Table
