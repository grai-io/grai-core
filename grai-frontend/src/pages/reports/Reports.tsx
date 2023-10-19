import React from "react"
import { gql, useQuery } from "@apollo/client"
import { useSearchParams } from "react-router-dom"
import getRepoFromParams from "helpers/getRepoFromParams"
import useWorkspace from "helpers/useWorkspace"
import PageHeader from "components/layout/PageHeader"
import PageTabs from "components/layout/PageTabs"
import ReportFilter from "components/reports/ReportFilter"
import ReportsTable from "components/reports/ReportsTable"
import TabState from "components/tabs/TabState"
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
        data {
          id
          type
          owner
          repo
          branches {
            data {
              id
              reference
            }
          }
          pull_requests {
            data {
              id
              reference
              title
            }
          }
        }
      }
      runs(
        filters: { owner: $owner, repo: $repo, branch: $branch, action: TESTS }
        order: { created_at: DESC }
      ) {
        data {
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
  }
`

const Reports: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()
  const [searchParams] = useSearchParams()

  const branch = searchParams.get("branch")
  const { owner, repo } = getRepoFromParams(searchParams)

  const { loading, error, data, refetch } = useQuery<
    GetReports,
    GetReportsVariables
  >(GET_REPORTS, {
    variables: {
      organisationName,
      workspaceName,
      owner,
      repo,
      branch,
    },
  })

  if (error) return <GraphError error={error} />

  const handleRefresh = () => refetch()

  const tabs = [
    {
      label: "All",
      value: "all",
      component: (
        <>
          <ReportFilter
            workspace={data?.workspace ?? null}
            onRefresh={handleRefresh}
          />
          <ReportsTable
            runs={data?.workspace.runs.data ?? null}
            loading={loading}
          />
        </>
      ),
    },
    {
      label: "Pulls",
      value: "pulls",
      disabled: true,
    },
    {
      label: "Commits",
      value: "commits",
      disabled: true,
    },
  ]

  return (
    <TabState tabs={tabs}>
      <PageHeader title="Reports" tabs />
      <PageTabs />
    </TabState>
  )
}

export default Reports
