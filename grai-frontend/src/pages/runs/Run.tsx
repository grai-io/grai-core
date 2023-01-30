import { gql, useQuery } from "@apollo/client"
import PageLayout from "components/layout/PageLayout"
import RunDetail from "components/runs/RunDetail"
import RunHeader from "components/runs/RunHeader"
import GraphError from "components/utils/GraphError"
import useWorkspace from "helpers/useWorkspace"
import NotFound from "pages/NotFound"
import React, { useEffect } from "react"
import { useParams } from "react-router-dom"
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
        connector {
          id
          name
        }
        connection {
          id
          name
          connector {
            id
            name
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

  useEffect(() => {
    switch (status) {
      case "queued":
      case "running":
        startPolling(1000)
        return

      case "success":
      case "error":
        stopPolling()
    }
  }, [status, startPolling, stopPolling])

  if (error) return <GraphError error={error} />
  if (loading) return <PageLayout loading />

  const run = data?.workspace?.run

  if (!run) return <NotFound />

  return (
    <PageLayout>
      <RunHeader run={run} />
      <RunDetail run={run} />
    </PageLayout>
  )
}
export default Run
