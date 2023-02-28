import React from "react"
import { gql, useQuery } from "@apollo/client"
import useRunPolling from "helpers/runPolling"
import useWorkspace from "helpers/useWorkspace"
import { useParams } from "react-router-dom"
import NotFound from "pages/NotFound"
import PageLayout from "components/layout/PageLayout"
import RunDetail from "components/runs/RunDetail"
import RunHeader from "components/runs/RunHeader"
import GraphError from "components/utils/GraphError"
import { GetRun, GetRunVariables } from "./__generated__/GetRun"

export const GET_RUN = gql`
  query GetRun(
    $organisationName: String!
    $workspaceName: String!
    $runId: ID!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      run(id: $runId) {
        id
        connection {
          id
          name
          connector {
            id
            name
          }
          runs(order: { created_at: DESC }) {
            id
            status
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
          last_run {
            id
            status
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
          last_successful_run {
            id
            status
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
        status
        metadata
        created_at
        updated_at
        started_at
        finished_at
        user {
          id
          username
          first_name
          last_name
        }
      }
    }
  }
`

const Run: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()
  const { runId } = useParams()

  const { loading, error, data, startPolling, stopPolling } = useQuery<
    GetRun,
    GetRunVariables
  >(GET_RUN, {
    variables: {
      organisationName,
      workspaceName,
      runId: runId ?? "",
    },
  })

  const status = data?.workspace.run?.status

  useRunPolling(status, startPolling, stopPolling)

  if (error) return <GraphError error={error} />
  if (loading) return <PageLayout loading />

  const run = data?.workspace?.run

  if (!run) return <NotFound />

  return (
    <PageLayout>
      <RunHeader run={run} workspaceId={data.workspace.id} />
      <RunDetail run={run} />
    </PageLayout>
  )
}
export default Run
