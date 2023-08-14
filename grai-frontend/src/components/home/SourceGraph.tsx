import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Box, Button, CircularProgress, Typography } from "@mui/material"
import { Link } from "react-router-dom"
import PageContent from "components/layout/PageContent"
import Graph from "components/sources/Graph"
import GraphError from "components/utils/GraphError"

export const GET_WORKSPACE_SOURCE_GRAPH = gql`
  query GetWorkspaceSourceGraph($workspaceId: ID!) {
    workspace(id: $workspaceId) {
      id
      source_graph {
        id
        name
        icon
        targets
      }
    }
  }
`

type SourceGraphProps = {
  workspaceId: string
}

const SourceGraph: React.FC<SourceGraphProps> = ({ workspaceId }) => {
  const { loading, error, data } = useQuery(GET_WORKSPACE_SOURCE_GRAPH, {
    variables: {
      workspaceId,
    },
  })

  if (error) return <GraphError error={error} />

  return (
    <PageContent noGutter noPadding>
      <Box sx={{ display: "flex", mb: 2, pt: "24px", mx: "24px" }}>
        <Typography
          sx={{ fontWeight: 800, fontSize: "20px", flexGrow: 1 }}
          variant="h5"
        >
          Sources
        </Typography>
        <Button
          component={Link}
          to="sources"
          size="large"
          sx={{ color: "#8338EC", fontWeight: 600, fontSize: "16px", mt: -1 }}
        >
          Explore all Sources
        </Button>
      </Box>
      {loading ? (
        <CircularProgress />
      ) : (
        <Box sx={{ height: "500px" }}>
          <Graph sourceGraph={data.workspace.source_graph} />
        </Box>
      )}
    </PageContent>
  )
}

export default SourceGraph
