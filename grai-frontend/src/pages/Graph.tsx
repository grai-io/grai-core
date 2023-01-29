import React from "react"
import { Alert, Box } from "@mui/material"
import GraphComponent, { Error } from "components/graph/Graph"
import { gql, useQuery } from "@apollo/client"
import theme from "theme"
import { useLocation, useParams } from "react-router-dom"
import GraphError from "components/utils/GraphError"
import PageLayout from "components/layout/PageLayout"
import {
  GetTablesAndEdges,
  GetTablesAndEdgesVariables,
} from "./__generated__/GetTablesAndEdges"

export const GET_TABLES_AND_EDGES = gql`
  query GetTablesAndEdges($workspaceId: ID!) {
    workspace(pk: $workspaceId) {
      id
      tables(pagination: { offset: 0, limit: 100000 }) {
        id
        namespace
        name
        display_name
        data_source
        metadata
        columns {
          id
          name
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

const Graph: React.FC = () => {
  const { workspaceId } = useParams()
  const searchParams = new URLSearchParams(useLocation().search)

  const { loading, error, data } = useQuery<
    GetTablesAndEdges,
    GetTablesAndEdgesVariables
  >(GET_TABLES_AND_EDGES, {
    variables: {
      workspaceId: workspaceId ?? "",
    },
  })

  if (error) return <GraphError error={error} />
  if (loading) return <PageLayout loading />

  const errorsQS = searchParams.get("errors")
  const errors: Error[] | null = errorsQS ? JSON.parse(errorsQS) : null
  const limitGraph: boolean =
    searchParams.get("limitGraph")?.toLowerCase() === "true" && !!errors

  const tables = data?.workspace.tables
  const edges = data?.workspace.other_edges ?? []

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
        <GraphComponent
          tables={tables}
          edges={edges}
          errors={errors}
          limitGraph={limitGraph}
        />
      </Box>
    </PageLayout>
  )
}

export default Graph
