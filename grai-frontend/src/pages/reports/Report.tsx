import React from "react"
import { gql, useQuery } from "@apollo/client"
import resultsToErrors from "helpers/resultsToErrors"
import useWorkspace from "helpers/useWorkspace"
import { useParams } from "react-router-dom"
import NotFound from "pages/NotFound"
import PageLayout from "components/layout/PageLayout"
import ReportBody from "components/reports/ReportBody"
import ReportRunHeader from "components/reports/run/ReportRunHeader"
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

const Report: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()
  const { reportId } = useParams()

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

  const tables = data?.workspace.tables
  const edges = data?.workspace.other_edges

  return (
    <PageLayout>
      <ReportRunHeader run={run} />
      <ReportBody tables={tables} edges={edges} errors={errors} />
    </PageLayout>
  )
}

export default Report
