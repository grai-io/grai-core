import React, { useState } from "react"
import { gql, useQuery } from "@apollo/client"
import useWorkspace from "helpers/useWorkspace"
import PageContent from "components/layout/PageContent"
import PageHeader from "components/layout/PageHeader"
import PageLayout from "components/layout/PageLayout"
import TableHeader from "components/nodes/NodeHeader"
import RunsTable from "components/runs/RunsTable"
import GraphError from "components/utils/GraphError"
import { GetRuns, GetRunsVariables } from "./__generated__/GetRuns"

export const GET_RUNS = gql`
  query GetRuns($organisationName: String!, $workspaceName: String!) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
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

const Runs: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()
  const [search, setSearch] = useState<string>()

  const { loading, error, data, refetch } = useQuery<GetRuns, GetRunsVariables>(
    GET_RUNS,
    {
      variables: {
        organisationName,
        workspaceName,
      },
    },
  )

  const handleRefresh = () => refetch()

  if (error) return <GraphError error={error} />

  const runs = data?.workspace.runs.data ?? []

  const filteredRuns = search
    ? runs.filter(run => run.id.toLowerCase().includes(search.toLowerCase()))
    : runs

  return (
    <PageLayout>
      <PageHeader title="Runs" />
      <PageContent>
        <TableHeader
          search={search}
          onSearch={setSearch}
          onRefresh={handleRefresh}
        />
        <RunsTable runs={filteredRuns} loading={loading} />
      </PageContent>
    </PageLayout>
  )
}

export default Runs
