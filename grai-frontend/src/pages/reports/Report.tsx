import React, { useEffect, useState } from "react"
import { gql, useQuery } from "@apollo/client"
import { useParams } from "react-router-dom"
import NotFound from "pages/NotFound"
import resultsToErrors from "helpers/resultsToErrors"
import useWorkspace from "helpers/useWorkspace"
import PageLayout from "components/layout/PageLayout"
import ReportBody from "components/reports/ReportBody"
import ReportRunHeader from "components/reports/run/ReportRunHeader"
import GraphError from "components/utils/GraphError"
import {
  GetRunReport,
  GetRunReportVariables,
} from "./__generated__/GetRunReport"
import PageHeader from "components/layout/PageHeader"
import ReportTabs2 from "components/reports/ReportTabs2"
import { Box, Stack, Typography } from "@mui/material"
import { durationAgo } from "helpers/runDuration"
import Graph from "components/graph/Graph"
import useSearchParams from "helpers/useSearchParams"

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

  const failureCount = errors?.filter(error => !error.test_pass).length ?? 0
  const passCount = errors?.filter(error => error.test_pass).length ?? 0
  const total = failureCount + passCount

  const limitGraph: boolean =
    searchParams.get("limitGraph")?.toLowerCase() === "true"

  if (!display) return null

  return (
    <PageLayout>
      <PageHeader
        title={`Run ${run.id.slice(0, 6)}`}
        tabs={<ReportTabs2 />}
        status={
          run.created_at && (
            <Typography>{`about ${durationAgo(
              run.created_at,
              1,
              true
            )} ago `}</Typography>
          )
        }
        buttons={
          <Stack direction="row" spacing={1}>
            <Typography>Failures</Typography>
            <Typography sx={{ mr: 3 }}>{failureCount}</Typography>
            <Typography>Passes</Typography>
            <Typography sx={{ mr: 3 }}>{passCount}</Typography>
            <Typography>Success Rate</Typography>
            <Typography sx={{ mr: 3 }}>
              {total > 0 ? (passCount / total) * 100 + "%" : "-"}
            </Typography>
          </Stack>
        }
      />
      <Box
        sx={{
          height: "calc(100vh - 144px)",
        }}
      >
        <Graph
          tables={tables}
          edges={edges}
          errors={errors}
          limitGraph={limitGraph}
        />
      </Box>
    </PageLayout>
  )
}

export default Report
