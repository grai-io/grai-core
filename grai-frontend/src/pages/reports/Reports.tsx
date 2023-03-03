import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Box } from "@mui/material"
import getRepoFromParams from "helpers/getRepoFromParams"
import useWorkspace from "helpers/useWorkspace"
import { useSearchParams } from "react-router-dom"
import PageLayout from "components/layout/PageLayout"
import ReportFilter from "components/reports/ReportFilter"
import ReportsHeader from "components/reports/ReportsHeader"
import ReportsTable from "components/reports/ReportsTable"
import ReportTabs from "components/reports/ReportTabs"
import GraphError from "components/utils/GraphError"
import { GetReports, GetReportsVariables } from "./__generated__/GetReports"

export const GET_REPORTS = gql`
  query GetReports(
    $organisationName: String!
    $workspaceName: String!
    $owner: String
    $repo: String
    $branch: String
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      repositories {
        id
        type
        owner
        repo
        branches {
          id
          reference
        }
        pull_requests {
          id
          reference
          title
        }
      }
      connections {
        id
        name
      }
      runs(owner: $owner, repo: $repo, branch: $branch, action: "tests") {
        id
        status
        connection {
          id
          name
          temp
          connector {
            id
            name
            icon
          }
        }
        commit {
          id
          reference
          title
          branch {
            id
            reference
          }
          pull_request {
            id
            reference
            title
          }
          repository {
            id
            type
            owner
            repo
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

const Reports: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()
  const [searchParams] = useSearchParams()

  const branch = searchParams.get("branch")
  const { owner, repo } = getRepoFromParams(searchParams)

  const { loading, error, data } = useQuery<GetReports, GetReportsVariables>(
    GET_REPORTS,
    {
      variables: {
        organisationName,
        workspaceName,
        owner,
        repo,
        branch,
      },
    }
  )

  if (error) return <GraphError error={error} />

  return (
    <PageLayout>
      <ReportsHeader />
      <Box sx={{ mx: 3 }}>
        <ReportTabs currentTab="all" />
        <ReportFilter workspace={data?.workspace ?? null} />
        <ReportsTable runs={data?.workspace.runs ?? null} loading={loading} />
      </Box>
    </PageLayout>
  )
}

export default Reports
