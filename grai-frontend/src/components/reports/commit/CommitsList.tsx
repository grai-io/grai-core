import React from "react"
import { gql, useQuery } from "@apollo/client"
import useWorkspace from "helpers/useWorkspace"
import { useParams } from "react-router-dom"
import NotFound from "pages/NotFound"
import Loading from "components/layout/Loading"
import GraphError from "components/utils/GraphError"
import {
  GetBranchCommits,
  GetBranchCommitsVariables,
} from "./__generated__/GetBranchCommits"
import { Repository } from "./CommitBreadcrumbs"
import CommitsTable from "./CommitsTable"

export const GET_BRANCH_COMMITS = gql`
  query GetBranchCommits(
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
        branch(reference: $reference) {
          id
          commits {
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
      }
    }
  }
`

type CommitsListProps = {
  type: string
  repository: Repository
  reference: string
}

const CommitsList: React.FC<CommitsListProps> = ({
  type,
  repository,
  reference,
}) => {
  const { organisationName, workspaceName } = useWorkspace()
  const params = useParams()

  const { loading, error, data } = useQuery<
    GetBranchCommits,
    GetBranchCommitsVariables
  >(GET_BRANCH_COMMITS, {
    variables: {
      organisationName,
      workspaceName,
      type,
      owner: params.owner ?? "",
      repo: params.repo ?? "",
      reference,
    },
  })

  if (error) return <GraphError error={error} />
  if (loading) return <Loading />

  const branch = data?.workspace.repository?.branch

  if (!branch) return <NotFound />

  return (
    <CommitsTable
      commits={branch.commits}
      type={type}
      repository={repository}
    />
  )
}

export default CommitsList
