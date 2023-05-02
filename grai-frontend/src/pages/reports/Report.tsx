import React, { useEffect, useState } from "react"
import { gql, useQuery } from "@apollo/client"
import { CallSplit, OpenInNew } from "@mui/icons-material"
import { Box, Link, Typography } from "@mui/material"
import { useParams } from "react-router-dom"
import NotFound from "pages/NotFound"
import resultsToErrors from "helpers/resultsToErrors"
import { durationAgo } from "helpers/runDuration"
import useSearchParams from "helpers/useSearchParams"
import useWorkspace from "helpers/useWorkspace"
import PageHeader from "components/layout/PageHeader"
import PageLayout from "components/layout/PageLayout"
import PageTabs from "components/layout/PageTabs"
import ReportResult from "components/reports/ReportResult"
import reportTabs from "components/reports/reportTabs"
import RunBreadcrumbs from "components/reports/run/RunBreadcrumbs"
import TabState from "components/tabs/TabState"
import GraphError from "components/utils/GraphError"
import {
  GetRunReport,
  GetRunReportVariables,
} from "./__generated__/GetRunReport"

export const GET_RUN = gql`
  query GetRunReport(
    $organisationName: String!
    $workspaceName: String!
    $runId: ID!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      run(id: $runId) {
        id
        metadata
        created_at
        commit {
          id
          reference
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
      }
      tables {
        data {
          id
          namespace
          name
          display_name
          data_source
          metadata
          columns {
            data {
              id
              name
            }
          }
          source_tables {
            data {
              id
              name
              display_name
            }
          }
          destination_tables {
            data {
              id
              name
              display_name
            }
          }
        }
      }
      other_edges {
        data {
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
  }
`

const Report: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()
  const { reportId } = useParams()

  const { searchParams, setSearchParams } = useSearchParams()
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

  const { loading, error, data } = useQuery<
    GetRunReport,
    GetRunReportVariables
  >(GET_RUN, {
    variables: {
      organisationName,
      workspaceName,
      runId: reportId ?? "",
    },
  })

  if (error) return <GraphError error={error} />
  if (loading) return <PageLayout loading />

  const run = data?.workspace.run

  if (!run) return <NotFound />

  const errors = resultsToErrors(run.metadata.results)

  const tables = data?.workspace.tables.data
  const edges = data?.workspace.other_edges.data

  const limitGraph: boolean =
    searchParams.get("limitGraph")?.toLowerCase() === "true"

  if (!display) return null

  const tabs = reportTabs({ tables, edges, errors, limitGraph, run })

  return (
    <PageLayout>
      <TabState tabs={tabs}>
        <PageHeader
          title={`Run ${run.id.slice(0, 6)}`}
          breadcrumbs={
            run.commit && <RunBreadcrumbs repository={run.commit.repository} />
          }
          tabs
          status={
            run.created_at && (
              <Typography>{`about ${durationAgo(
                run.created_at,
                1,
                true
              )} ago `}</Typography>
            )
          }
          buttons={<ReportResult errors={errors} />}
        >
          {run.commit && (
            <Box sx={{ display: "flex", mt: 2 }}>
              <Typography variant="body2" sx={{ display: "flex" }}>
                {run.commit?.pull_request && (
                  <Link
                    href={`https://github.com/${run.commit.repository.owner}/${run.commit.repository.repo}/pull/${run.commit.pull_request.reference}`}
                    target="_blank"
                    underline="hover"
                    sx={{ display: "flex", alignItems: "center", ml: 0.5 }}
                  >
                    <span>
                      {run.commit.pull_request.title} #
                      {run.commit.pull_request.reference}
                    </span>
                    <OpenInNew sx={{ fontSize: 15, ml: 0.25 }} />
                  </Link>
                )}
              </Typography>
              {run.commit?.branch && (
                <Typography
                  variant="body2"
                  sx={{ ml: 1, display: "flex", alignItems: "center" }}
                >
                  <CallSplit sx={{ fontSize: 15, mx: 0.25 }} />
                  {run.commit.branch.reference}
                </Typography>
              )}
            </Box>
          )}
        </PageHeader>
        <PageTabs />
      </TabState>
    </PageLayout>
  )
}

export default Report
