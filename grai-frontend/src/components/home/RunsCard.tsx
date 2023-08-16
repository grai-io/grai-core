import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Box, Button, CircularProgress, Typography } from "@mui/material"
import { Link } from "react-router-dom"
import PageContent from "components/layout/PageContent"
import RunsTable from "components/runs/RunsTable"
import GraphError from "components/utils/GraphError"
import {
  GetWorkspaceRuns,
  GetWorkspaceRunsVariables,
} from "./__generated__/GetWorkspaceRuns"

export const GET_RUNS = gql`
  query GetWorkspaceRuns($workspaceId: ID!) {
    workspace(id: $workspaceId) {
      id
      runs(order: { created_at: DESC }) {
        data {
          id
          status
          connection {
            id
            name
            connector {
              id
              name
            }
          }
          created_at
          started_at
          finished_at
          user {
            id
            first_name
            last_name
          }
          metadata
        }
      }
    }
  }
`

type RunsCardProps = {
  workspaceId: string
}

const RunsCard: React.FC<RunsCardProps> = ({ workspaceId }) => {
  const { loading, error, data } = useQuery<
    GetWorkspaceRuns,
    GetWorkspaceRunsVariables
  >(GET_RUNS, {
    variables: {
      workspaceId,
    },
  })

  if (error) return <GraphError error={error} />

  return (
    <PageContent noGutter>
      <Box sx={{ display: "flex", mb: 2 }}>
        <Typography
          sx={{ fontWeight: 800, fontSize: "20px", flexGrow: 1 }}
          variant="h5"
        >
          Runs
        </Typography>
        <Button
          component={Link}
          to="runs"
          size="large"
          sx={{ color: "#8338EC", fontWeight: 600, fontSize: "16px", mt: -1 }}
        >
          Explore all Runs
        </Button>
      </Box>
      {loading ? (
        <CircularProgress />
      ) : (
        <Box sx={{ height: "500px" }}>
          <RunsTable runs={data?.workspace.runs.data ?? []} />
        </Box>
      )}
    </PageContent>
  )
}

export default RunsCard
