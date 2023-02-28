import React from "react"
import { gql, useQuery } from "@apollo/client"
import useWorkspace from "helpers/useWorkspace"
import { useParams } from "react-router-dom"
import NotFound from "pages/NotFound"
import PageLayout from "components/layout/PageLayout"
import TableContent from "components/tables/TableContent"
import TableHeader from "components/tables/TableHeader"
import GraphError from "components/utils/GraphError"
import { GetTable, GetTableVariables } from "./__generated__/GetTable"

export const GET_TABLE = gql`
  query GetTable(
    $organisationName: String!
    $workspaceName: String!
    $tableId: ID!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      table(id: $tableId) {
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
          requirements_edges {
            id
            metadata
            source {
              id
              name
              display_name
              metadata
            }
          }
          metadata
        }
        source_tables {
          id
          name
          display_name
        }
        destination_tables {
          id
          name
          display_name
        }
      }
    }
  }
`

const Table: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()
  const { tableId } = useParams()

  const { loading, error, data } = useQuery<GetTable, GetTableVariables>(
    GET_TABLE,
    {
      variables: {
        organisationName,
        workspaceName,
        tableId: tableId ?? "",
      },
    }
  )

  if (error) return <GraphError error={error} />
  if (loading) return <PageLayout loading />

  const table = data?.workspace?.table

  if (!table) return <NotFound />

  return (
    <PageLayout>
      <TableHeader table={table} />
      <TableContent table={table} />
    </PageLayout>
  )
}

export default Table
