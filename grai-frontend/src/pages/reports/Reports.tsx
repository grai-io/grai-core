import { gql, useQuery } from "@apollo/client"
import { Box } from "@mui/material"
import PageLayout from "components/layout/PageLayout"
import CommitsTable from "components/reports/CommitsTable"
import ReportHeader from "components/reports/ReportHeader"
import ReportTabs from "components/reports/ReportTabs"
import GraphError from "components/utils/GraphError"
import useWorkspace from "helpers/useWorkspace"
import NotFound from "pages/NotFound"
import React from "react"
import { useParams } from "react-router-dom"
import { GetCommits, GetCommitsVariables } from "./__generated__/GetCommits"

export const GET_COMMITS = gql`
  query GetCommits(
    $organisationName: String!
    $workspaceName: String!
    $type: String!
    $owner: String!
    $repo: String!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      repository(type: $type, owner: $owner, repo: $repo) {
        id
        owner
        repo
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
`

const Reports: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()
  const params = useParams()

  const type = params.type ?? ""

  const { loading, error, data } = useQuery<GetCommits, GetCommitsVariables>(
    GET_COMMITS,
    {
      variables: {
        organisationName,
        workspaceName,
        type,
        owner: params.owner ?? "",
        repo: params.repo ?? "",
      },
    }
  )

  if (error) return <GraphError error={error} />
  if (loading) return <PageLayout loading />

  const repository = data?.workspace.repository

  if (!repository) return <NotFound />

  return (
    <PageLayout>
      <ReportHeader type={type} repository={repository} />
      <Box sx={{ px: 2 }}>
        <ReportTabs currentTab="commits" type={type} repository={repository} />
        <CommitsTable
          commits={repository.commits}
          type={type}
          repository={repository}
        />
      </Box>
    </PageLayout>
  )
}

export default Reports
