import React, { useEffect, useState } from "react"
import { gql, useQuery } from "@apollo/client"
import { CallSplit, OpenInNew } from "@mui/icons-material"
import { Box, Link, Typography } from "@mui/material"
import { useParams, useSearchParams } from "react-router-dom"
import NotFound from "pages/NotFound"
import resultsToErrors from "helpers/resultsToErrors"
import { durationAgo } from "helpers/runDuration"
import useWorkspace from "helpers/useWorkspace"
import PageHeader from "components/layout/PageHeader"
import PageLayout from "components/layout/PageLayout"
import PageTabs from "components/layout/PageTabs"
import PullRequestBreadcrumbs from "components/reports/pull_request/PullRequestBreadcrumbs"
import ReportResult from "components/reports/ReportResult"
import reportTabs from "components/reports/reportTabs"
import TabState from "components/tabs/TabState"
import GraphError from "components/utils/GraphError"
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
              created_at
            }
          }
          branch {
            id
            reference
          }
        }
      }
      graph {
        id
        name
        display_name
        namespace
        x
        y
        data_source
        columns {
          id
          name
          display_name
          destinations
        }
        destinations
      }
      filters {
        data {
          id
          name
        }
      }
    }
  }
`

const PullRequest: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()
  const params = useParams()
  const [searchParams, setSearchParams] = useSearchParams()
  const [display, setDisplay] = useState(false)

  useEffect(() => {
    setSearchParams(
      { ...searchParams, limitGraph: "true" },
      {
        replace: true,
      }
    )
    setDisplay(true)
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

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

  const limitGraph: boolean =
    searchParams.get("limitGraph")?.toLowerCase() === "true"

  if (error) return <GraphError error={error} />
  if (loading) return <PageLayout loading />

  const pullRequest = data?.workspace.repository.pull_request

  if (!pullRequest) return <NotFound />

  const run = pullRequest.last_commit?.last_successful_run ?? null
  const errors = resultsToErrors(run?.metadata.results)

  const tables = data?.workspace.graph

  if (!display) return null

  const tabs = reportTabs({ tables, errors, limitGraph, run })

  return (
    <PageLayout>
      <TabState tabs={tabs}>
        <PageHeader
          title={pullRequest.title ?? `Run ${run?.id.slice(0, 6)}`}
          breadcrumbs={
            <PullRequestBreadcrumbs
              type={type}
              repository={data.workspace.repository}
              reference={pullRequest.reference}
            />
          }
          status={
            run?.created_at && (
              <Typography>{`about ${durationAgo(
                run.created_at,
                1,
                true
              )} ago `}</Typography>
            )
          }
          buttons={<ReportResult errors={errors} />}
          tabs
        >
          <Box sx={{ display: "flex", mt: 2 }}>
            <Typography variant="body2" sx={{ display: "flex" }}>
              <Link
                href={`https://github.com/${data.workspace.repository.owner}/${data.workspace.repository.repo}/pull/${pullRequest.reference}`}
                target="_blank"
                underline="hover"
                sx={{ display: "flex", alignItems: "center", ml: 0.5 }}
              >
                <span>#{pullRequest.reference}</span>
                <OpenInNew sx={{ fontSize: 15, ml: 0.25 }} />
              </Link>
            </Typography>
            <Typography
              variant="body2"
              sx={{ ml: 1, display: "flex", alignItems: "center" }}
            >
              <CallSplit sx={{ fontSize: 15, mx: 0.25 }} />
              {pullRequest.branch.reference}
            </Typography>
          </Box>
        </PageHeader>
        <PageTabs />
      </TabState>
    </PageLayout>
  )
}

export default PullRequest
