import React from "react"
import { gql, useQuery } from "@apollo/client"
import { useParams } from "react-router-dom"
import NotFound from "pages/NotFound"
import useRunPolling from "helpers/runPolling"
import useWorkspace from "helpers/useWorkspace"
import ConnectionRun, { RunResult } from "components/connections/ConnectionRun"
import PageContent from "components/layout/PageContent"
import PageHeader from "components/layout/PageHeader"
import PageLayout from "components/layout/PageLayout"
import RunDetail from "components/runs/RunDetail"
import RunStatus from "components/runs/RunStatus"
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
            events
          }
          runs(order: { created_at: DESC }) {
            data {
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
  const { organisationName, workspaceName, workspaceNavigate } = useWorkspace()
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

  const handleRun = (run: RunResult) => workspaceNavigate(`runs/${run.id}`)

  return (
    <PageLayout>
      <PageHeader
        title={
          (run.connection ? run.connection.name + "/" : null) +
          run.id.slice(0, 6)
        }
        status={<RunStatus run={run} sx={{ ml: 2 }} />}
        buttons={
          run.connection && (
            <ConnectionRun
              connection={run.connection}
              workspaceId={data.workspace.id}
              onRun={handleRun}
            />
          )
        }
      />
      <PageContent>
        <RunDetail run={run} />
      </PageContent>
    </PageLayout>
  )
}
export default Run
