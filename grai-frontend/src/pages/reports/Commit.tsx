import React from "react"
import { gql, useQuery } from "@apollo/client"
import resultsToErrors from "helpers/resultsToErrors"
import useWorkspace from "helpers/useWorkspace"
import { useParams } from "react-router-dom"
import NotFound from "pages/NotFound"
import PageLayout from "components/layout/PageLayout"
import CommitHeader from "components/reports/commit/CommitHeader"
import ReportBody from "components/reports/ReportBody"
import GraphError from "components/utils/GraphError"
import { GetCommit, GetCommitVariables } from "./__generated__/GetCommit"

export const GET_COMMIT = gql`
  query GetCommit(
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
        commit(reference: $reference) {
          id
          reference
          title
          created_at
          last_successful_run {
            id
            metadata
          }
          branch {
            id
            reference
          }
          pull_request {
            id
            reference
            title
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

const Commit: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()
  const params = useParams()

  const type = params.type ?? ""

  const { loading, error, data } = useQuery<GetCommit, GetCommitVariables>(
    GET_COMMIT,
    {
      variables: {
        organisationName,
        workspaceName,
        type,
        owner: params.owner ?? "",
        repo: params.repo ?? "",
        reference: params.reference ?? "",
      },
    }
  )

  if (error) return <GraphError error={error} />
  if (loading) return <PageLayout loading />

  const commit = data?.workspace.repository.commit

  if (!commit) return <NotFound />

  const errors = resultsToErrors(commit.last_successful_run?.metadata.results)

  const tables = data?.workspace.tables
  const edges = data?.workspace.other_edges

  return (
    <PageLayout>
      <CommitHeader
        type={type}
        repository={data.workspace.repository}
        commit={commit}
      />
      <ReportBody tables={tables} edges={edges} errors={errors} />
    </PageLayout>
  )
}

export default Commit
