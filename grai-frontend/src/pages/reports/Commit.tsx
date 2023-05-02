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
import CommitBreadcrumbs from "components/reports/commit/CommitBreadcrumbs"
import ReportResult from "components/reports/ReportResult"
import reportTabs from "components/reports/reportTabs"
import TabState from "components/tabs/TabState"
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
            created_at
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

const Commit: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()
  const params = useParams()

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

  const run = commit.last_successful_run
  const errors = resultsToErrors(run?.metadata.results)

  const tables = data?.workspace.tables.data
  const edges = data?.workspace.other_edges.data

  const limitGraph: boolean =
    searchParams.get("limitGraph")?.toLowerCase() === "true"

  if (!display) return null

  const tabs = reportTabs({ tables, edges, errors, limitGraph, run })

  const repository = data.workspace.repository

  return (
    <PageLayout>
      <TabState tabs={tabs}>
        <PageHeader
          title={commit.title ?? `Run ${run?.id.slice(0, 6)}`}
          breadcrumbs={
            <CommitBreadcrumbs
              type={type}
              repository={repository}
              reference={commit.reference}
            />
          }
          tabs
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
        >
          <Box sx={{ display: "flex", mt: 2 }}>
            <Typography variant="body2" sx={{ display: "flex" }}>
              <Link
                href={
                  commit.pull_request
                    ? `https://github.com/${repository.owner}/${repository.repo}/pull/${commit.pull_request.reference}/commits/${commit.reference}`
                    : `https://github.com/${repository.owner}/${repository.repo}/tree/${commit.reference}`
                }
                target="_blank"
                underline="hover"
                sx={{ display: "flex", alignItems: "center", ml: 0.5 }}
              >
                <span>#{commit.reference.slice(0, 7)}</span>
                <OpenInNew sx={{ fontSize: 15, ml: 0.25 }} />
              </Link>
            </Typography>
            <Typography
              variant="body2"
              sx={{ ml: 1, display: "flex", alignItems: "center" }}
            >
              <CallSplit sx={{ fontSize: 15, mx: 0.25 }} />
              {commit.branch.reference}
            </Typography>
          </Box>
        </PageHeader>
        <PageTabs />
      </TabState>
    </PageLayout>
  )
}

export default Commit
