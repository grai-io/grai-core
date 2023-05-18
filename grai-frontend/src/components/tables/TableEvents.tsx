import React from "react"
import { gql, useQuery } from "@apollo/client"
import NotFound from "pages/NotFound"
import useWorkspace from "helpers/useWorkspace"
import ConnectionEventPlots from "components/connections/events/ConnectionEventPlots"
import ConnectionEventsTable from "components/connections/events/ConnectionEventsTable"
import Loading from "components/layout/Loading"
import PageContent from "components/layout/PageContent"
import GraphError from "components/utils/GraphError"
import {
  GetTableEvents,
  GetTableEventsVariables,
} from "./__generated__/GetTableEvents"

export const GET_TABLE_EVENTS = gql`
  query GetTableEvents(
    $organisationName: String!
    $workspaceName: String!
    $tableId: ID!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      table(id: $tableId) {
        id
        events {
          data {
            id
            date
            status
            connection {
              id
              name
              connector {
                id
                name
                icon
              }
            }
          }
          meta {
            total
          }
        }
      }
    }
  }
`

interface Table {
  id: string
}

type TableEventsProps = {
  table: Table
  responsive?: boolean
}

const TableEvents: React.FC<TableEventsProps> = ({ table, responsive }) => {
  const { organisationName, workspaceName } = useWorkspace()

  const { loading, error, data } = useQuery<
    GetTableEvents,
    GetTableEventsVariables
  >(GET_TABLE_EVENTS, {
    variables: {
      organisationName,
      workspaceName,
      tableId: table.id,
    },
  })

  if (error) return <GraphError error={error} />
  if (loading) return <Loading />

  const tableData = data?.workspace?.table

  if (!tableData) return <NotFound />

  const events = tableData.events.data

  return (
    <>
      <PageContent>
        <ConnectionEventPlots events={events} responsive={responsive} />
      </PageContent>
      <PageContent>
        <ConnectionEventsTable
          events={events}
          total={tableData.events.meta.total}
          connections
        />
      </PageContent>
    </>
  )
}

export default TableEvents
