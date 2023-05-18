import React from "react"
import { gql, useQuery } from "@apollo/client"
import { useParams } from "react-router-dom"
import NotFound from "pages/NotFound"
import useWorkspace from "helpers/useWorkspace"
import PageContent from "components/layout/PageContent"
import PageHeader from "components/layout/PageHeader"
import PageLayout from "components/layout/PageLayout"
import PageTabs from "components/layout/PageTabs"
import TableColumns from "components/tables/columns/TableColumns"
import TableLineage from "components/tables/TableLineage"
import TableProfile from "components/tables/TableProfile"
import TabState from "components/tabs/TabState"
import GraphError from "components/utils/GraphError"
import { GetTable, GetTableVariables } from "./__generated__/GetTable"
import TableEvents from "components/tables/TableEvents"

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
          data {
            id
            name
            display_name
            requirements_edges {
              data {
                id
                metadata
                destination {
                  id
                  name
                  display_name
                  metadata
                }
              }
            }
            metadata
          }
        }
        source_tables {
          data {
            id
            name
            display_name
          }
        }
        destination_tables {
          data {
            id
            name
            display_name
          }
        }
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
              }
            }
          }
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

  const tabs = [
    {
      label: "Profile",
      value: "profile",
      component: (
        <>
          <PageContent>
            <TableProfile table={table} />
          </PageContent>
          <PageContent>
            <TableColumns columns={table.columns.data} />
          </PageContent>
        </>
      ),
      noWrapper: true,
    },
    {
      label: "Sample",
      value: "sample",
      disabled: true,
    },
    {
      label: "Lineage",
      value: "lineage",
      component: <TableLineage table={table} />,
      noWrapper: true,
    },
    {
      label: 'Events',
      value: 'events',
      component: <TableEvents table={table} />,
      noWrapper: true,
    }
  ]

  return (
    <PageLayout>
      <TabState tabs={tabs}>
        <PageHeader title={table.display_name} tabs />
        <PageTabs />
      </TabState>
    </PageLayout>
  )
}

export default Table
