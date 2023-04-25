import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Alert, Box, Button, Typography } from "@mui/material"
import { useSearchParams, Link } from "react-router-dom"
import theme from "theme"
import useWorkspace from "helpers/useWorkspace"
import GraphComponent, { Error } from "components/graph/Graph"
import PageLayout from "components/layout/PageLayout"
import GraphError from "components/utils/GraphError"
import {
  GetTablesAndEdges,
  GetTablesAndEdgesVariables,
} from "./__generated__/GetTablesAndEdges"

export const GET_TABLES_AND_EDGES = gql`
  query GetTablesAndEdges($organisationName: String!, $workspaceName: String!) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      tables {
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
    }
  }
`

const Graph: React.FC = () => {
  const { organisationName, workspaceName, routePrefix } = useWorkspace()
  const [searchParams] = useSearchParams()

  const { loading, error, data } = useQuery<
    GetTablesAndEdges,
    GetTablesAndEdgesVariables
  >(GET_TABLES_AND_EDGES, {
    variables: {
      organisationName,
      workspaceName,
    },
  })

  if (error) return <GraphError error={error} />
  if (loading) return <PageLayout loading />

  const errorsQS = searchParams.get("errors")
  const errors: Error[] | null = errorsQS ? JSON.parse(errorsQS) : null
  const limitGraph: boolean =
    searchParams.get("limitGraph")?.toLowerCase() === "true" && !!errors

  const tables = data?.workspace.tables.data
  const edges = data?.workspace.other_edges.data ?? []

  if (!tables) return <Alert>No tables found</Alert>

  return (
    <PageLayout>
      <Box
        sx={{
          height: "calc(100vh - 70px)",
          width: "100%",
          backgroundColor: theme.palette.grey[100],
        }}
      >
        {tables.length > 0 ? (
          <GraphComponent
            tables={tables}
            edges={edges}
            errors={errors}
            limitGraph={limitGraph}
          />
        ) : (
          <Box
            sx={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              height: "100%",
              flexDirection: "column",
            }}
          >
            <Typography sx={{ pb: 3 }}>Your graph is empty!</Typography>
            <Typography>
              To get started{" "}
              <Button
                component={Link}
                to={`${routePrefix}/connections/create`}
                variant="outlined"
                sx={{ ml: 1 }}
              >
                Add Connection
              </Button>
            </Typography>
          </Box>
        )}
      </Box>
    </PageLayout>
  )
}

export default Graph
