import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Box } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import PageLayout from "components/layout/PageLayout"
import RunsHeader from "components/runs/RunsHeader"
import RunsTable from "components/runs/RunsTable"
import GraphError from "components/utils/GraphError"
import { GetRuns, GetRunsVariables } from "./__generated__/GetRuns"

export const GET_RUNS = gql`
  query GetRuns($organisationName: String!, $workspaceName: String!) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      runs {
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
`

const Runs: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()

  const { loading, error, data, refetch } = useQuery<GetRuns, GetRunsVariables>(
    GET_RUNS,
    {
      variables: {
        organisationName,
        workspaceName,
      },
    }
  )

  const handleRefresh = () => refetch()

  if (error) return <GraphError error={error} />

  return (
    <PageLayout>
      <RunsHeader onRefresh={handleRefresh} />
      <Box
        sx={{
          px: 3,
        }}
      >
        <RunsTable runs={data?.workspace.runs ?? []} loading={loading} />
      </Box>
    </PageLayout>
  )
}

export default Runs
