import { gql, useQuery } from "@apollo/client"
import { Box } from "@mui/material"
import Graph from "components/graph/Graph"
import PageLayout from "components/layout/PageLayout"
import GraphError from "components/utils/GraphError"
import useWorkspace from "helpers/useWorkspace"
import NotFound from "pages/NotFound"
import React from "react"
import { useParams } from "react-router-dom"
import { Error } from "components/graph/Graph"
import PullRequestHeader from "components/reports/pull_request/PullRequestHeader"
import {
  GetPullRequest,
  GetPullRequestVariables,
} from "./__generated__/GetPullRequest"

export const GET_PULL_REQUEST = gql`
  query GetPullRequest(
    $organisationName: String!
    $workspaceName: String!
    $type: String!
    $owner: String!
    $repo: String!
    $reference: String!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      repository(type: $type, owner: $owner, repo: $repo) {
        id
        owner
        repo
        pull_request(reference: $reference) {
          id
          reference
          title
          last_commit {
            id
            reference
            created_at
            last_successful_run {
              id
              metadata
            }
          }
          branch {
            id
            reference
          }
        }
      }
      tables {
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

const PullRequest: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()
  const params = useParams()

  const type = params.type ?? ""

  const { loading, error, data } = useQuery<
    GetPullRequest,
    GetPullRequestVariables
  >(GET_PULL_REQUEST, {
    variables: {
      organisationName,
      workspaceName,
      type,
      owner: params.owner ?? "",
      repo: params.repo ?? "",
      reference: params.reference ?? "",
    },
  })

  if (error) return <GraphError error={error} />
  if (loading) return <PageLayout loading />

  const pullRequest = data?.workspace.repository.pull_request

  if (!pullRequest) return <NotFound />

  interface Node {
    id: string
    name: string
    namespace: string
  }

  interface Result {
    node: Node
    node_name: string
    failing_node: Node
    failing_node_name: string
    type: string
    message: string
  }

  const results: Result[] | undefined =
    pullRequest.last_commit?.last_successful_run?.metadata.results

  const errors: Error[] | null = results
    ? results.map(result => ({
        source: result.node.name,
        destination: result.failing_node.name,
        test: result.type,
        message: result.message,
      }))
    : null

  const tables = data?.workspace.tables
  const edges = data?.workspace.other_edges

  return (
    <PageLayout>
      <PullRequestHeader
        type={type}
        repository={data.workspace.repository}
        pullRequest={pullRequest}
      />
      <Box
        sx={{
          height: "calc(100vh - 186.002px)",
          width: "100%",
          backgroundColor: theme => theme.palette.grey[100],
        }}
      >
        <Graph tables={tables} edges={edges} errors={errors} limitGraph />
      </Box>
    </PageLayout>
  )
}

export default PullRequest
