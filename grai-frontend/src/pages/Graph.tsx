import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Box } from "@mui/material"
import { useSearchParams } from "react-router-dom"
import theme from "theme"
import useWorkspace from "helpers/useWorkspace"
import { ControlOptions } from "components/graph/controls/GraphControls"
import EmptyGraph from "components/graph/EmptyGraph"
import GraphComponent, { Error } from "components/graph/Graph"
import PageLayout from "components/layout/PageLayout"
import GraphError from "components/utils/GraphError"
import {
  GetTablesAndEdges,
  GetTablesAndEdgesVariables,
} from "./__generated__/GetTablesAndEdges"

export const GET_TABLES_AND_EDGES = gql`
  query GetTablesAndEdges(
    $organisationName: String!
    $workspaceName: String!
    $filters: WorkspaceTableFilter
    $offset: Int!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      tables(filters: $filters, pagination: { limit: 1000, offset: $offset }) {
        data {
          id
          namespace
          name
          display_name
          data_source
          metadata
          columns {
            data {
              id
              name
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
        meta {
          total
        }
      }
      other_edges {
        data {
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
      filters {
        data {
          id
          name
        }
      }
    }
  }
`

const Graph: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()
  const [searchParams] = useSearchParams()

  const filter = searchParams.get("filter") ?? null

  const { loading, error, data, fetchMore } = useQuery<
    GetTablesAndEdges,
    GetTablesAndEdgesVariables
  >(GET_TABLES_AND_EDGES, {
    variables: {
      organisationName,
      workspaceName,
      filters: {
        filter,
      },
      offset: 0,
    },
  })

  if (error) return <GraphError error={error} />

  const errorsQS = searchParams.get("errors")
  const errors: Error[] | null = errorsQS ? JSON.parse(errorsQS) : null
  const limitGraph: boolean =
    searchParams.get("limitGraph")?.toLowerCase() === "true" && !!errors

  const tables = data?.workspace.tables.data ?? []
  const edges = data?.workspace.other_edges.data ?? []

  const total = data?.workspace.tables.meta.total ?? 0

  // if (total > tables.length) {
  //   fetchMore({
  //     variables: {
  //       offset: tables.length,
  //     },
  //     updateQuery: (prevResult, { fetchMoreResult }) => ({
  //       workspace: {
  //         ...fetchMoreResult.workspace,
  //         tables: {
  //           ...fetchMoreResult.workspace.tables,
  //           data: [
  //             ...prevResult.workspace.tables.data,
  //             ...fetchMoreResult.workspace.tables.data,
  //           ],
  //         },
  //       },
  //     }),
  //   })
  // }

  const controlOptions: ControlOptions = {}

  if (total > tables.length) {
    controlOptions.loadMore = {
      count: tables.length,
      total,
      onLoadMore: () =>
        fetchMore({
          variables: {
            offset: tables.length,
          },
          updateQuery: (prevResult, { fetchMoreResult }) => ({
            workspace: {
              ...fetchMoreResult.workspace,
              tables: {
                ...fetchMoreResult.workspace.tables,
                data: [
                  ...prevResult.workspace.tables.data,
                  ...fetchMoreResult.workspace.tables.data,
                ],
              },
            },
          }),
        }),
    }
  }

  return (
    <PageLayout>
      <Box
        sx={{
          height: "100vh",
          width: "100%",
          backgroundColor: theme.palette.grey[100],
        }}
      >
        {total > 0 || loading ? (
          <GraphComponent
            tables={tables}
            edges={edges}
            errors={errors}
            limitGraph={limitGraph}
            loading={loading}
            controlOptions={controlOptions}
          />
        ) : (
          <EmptyGraph />
        )}
      </Box>
    </PageLayout>
  )
}

export default Graph
