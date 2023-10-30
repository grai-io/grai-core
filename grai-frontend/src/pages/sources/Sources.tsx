import React, { useState } from "react"
import { gql, useQuery } from "@apollo/client"
import useWorkspace from "helpers/useWorkspace"
import PageContent from "components/layout/PageContent"
import PageHeader from "components/layout/PageHeader"
import AddSourceButton from "components/sources/add_source/AddSourceButton"
import SourcesTable from "components/sources/SourcesTable"
import TableHeader from "components/table/TableHeader"
import GraphError from "components/utils/GraphError"
import { GetSources, GetSourcesVariables } from "./__generated__/GetSources"

export const GET_SOURCES = gql`
  query GetSources($organisationName: String!, $workspaceName: String!) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      sample_data
      organisation {
        id
      }
      sources {
        data {
          id
          name
          priority
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
              validated
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
  const { organisationName, workspaceName } = useWorkspace()

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

  const workspace = data?.workspace
  const sources = workspace?.sources.data ?? []

  const filteredSources = search
    ? sources.filter(source =>
        source.name.toLowerCase().includes(search.toLowerCase()),
      )
    : sources

  return (
    <>
      <PageHeader
        title="Sources"
        buttons={<AddSourceButton workspace={workspace} />}
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
          total={workspace?.sources.meta.total ?? 0}
        />
      </PageContent>
    </>
  )
}

export default Sources
