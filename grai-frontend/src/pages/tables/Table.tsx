import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Grid, Card, Table as BaseTable, TableBody } from "@mui/material"
import { useParams } from "react-router-dom"
import NotFound from "pages/NotFound"
import useTabs from "helpers/useTabs"
import useWorkspace from "helpers/useWorkspace"
import PageContent from "components/layout/PageContent"
import PageHeader from "components/layout/PageHeader"
import PageLayout from "components/layout/PageLayout"
import PageTabs from "components/layout/PageTabs"
import TableColumns from "components/tables/columns/TableColumns"
import TableDependencies from "components/tables/TableDependencies"
import TableDetail from "components/tables/TableDetail"
import TableLineage from "components/tables/TableLineage"
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
      }
    }
  }
`

const Table: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()
  const { tableId } = useParams()

  const { currentTab, setTab } = useTabs({ defaultTab: "profile" })

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
            <Grid container spacing={3}>
              <Grid item md={6}>
                <TableDetail table={table} />
              </Grid>
              <Grid item md={6}>
                <Card
                  variant="outlined"
                  sx={{ borderRadius: 0, borderBottom: 0 }}
                >
                  <BaseTable>
                    <TableBody>
                      <TableDependencies
                        label="Upstream dependencies"
                        dependencies={table.destination_tables.data}
                      />
                      <TableDependencies
                        label="Downstream dependencies"
                        dependencies={table.source_tables.data}
                      />
                    </TableBody>
                  </BaseTable>
                </Card>
              </Grid>
            </Grid>
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
  ]

  return (
    <PageLayout>
      <PageHeader
        title={table.display_name}
        tabs={tabs}
        currentTab={currentTab}
        setTab={setTab}
      />
      <PageTabs tabs={tabs} currentTab={currentTab} />
    </PageLayout>
  )
}

export default Table
