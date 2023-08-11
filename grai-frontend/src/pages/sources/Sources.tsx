import React, { useState } from "react"
import { gql, useQuery } from "@apollo/client"
import { Add } from "@mui/icons-material"
import { Button } from "@mui/material"
import { Link } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"
import PageContent from "components/layout/PageContent"
import PageHeader from "components/layout/PageHeader"
import PageLayout from "components/layout/PageLayout"
import TableHeader from "components/table/TableHeader"
import SourcesTable from "components/sources/SourcesTable"
import GraphError from "components/utils/GraphError"
import { GetSources, GetSourcesVariables } from "./__generated__/GetSources"

export const GET_SOURCES = gql`
  query GetSources($organisationName: String!, $workspaceName: String!) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      sources {
        data {
          id
          name
          nodes {
            meta {
              total
            }
          }
          edges {
            meta {
              total
            }
          }
          connections(filters: { temp: false }) {
            data {
              id
              name
              connector {
                id
                name
                icon
              }
              last_run {
                id
                status
              }
            }
          }
        }
        meta {
          total
        }
      }
    }
  }
`

const Sources: React.FC = () => {
  const [search, setSearch] = useState<string>()
  const { organisationName, workspaceName, routePrefix } = useWorkspace()

  const { loading, error, data, refetch } = useQuery<
    GetSources,
    GetSourcesVariables
  >(GET_SOURCES, {
    variables: {
      organisationName,
      workspaceName,
    },
  })

  const handleRefresh = () => refetch()

  if (error) return <GraphError error={error} />

  const sources = data?.workspace.sources.data ?? []

  const filteredSources = search
    ? sources.filter(source =>
        source.name.toLowerCase().includes(search.toLowerCase()),
      )
    : sources

  return (
    <PageLayout>
      <PageHeader
        title="Sources"
        buttons={
          <Button
            variant="contained"
            startIcon={<Add />}
            component={Link}
            to={`${routePrefix}/connections/create`}
            sx={{
              backgroundColor: "#FC6016",
              boxShadow: "0px 4px 6px rgba(252, 96, 22, 0.2)",
              borderRadius: "8px",
              height: "40px",
            }}
          >
            Add Source
          </Button>
        }
      />
      <PageContent>
        <TableHeader
          search={search}
          onSearch={setSearch}
          onRefresh={handleRefresh}
        />
        <SourcesTable
          sources={filteredSources}
          workspaceId={data?.workspace.id}
          loading={loading}
          total={data?.workspace.sources.meta.total ?? 0}
        />
      </PageContent>
    </PageLayout>
  )
}

export default Sources
