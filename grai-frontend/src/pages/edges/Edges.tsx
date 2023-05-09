import React, { useState } from "react"
import { gql, useQuery } from "@apollo/client"
import useWorkspace from "helpers/useWorkspace"
import EdgesTable from "components/edges/EdgesTable"
import PageContent from "components/layout/PageContent"
import PageHeader from "components/layout/PageHeader"
import PageLayout from "components/layout/PageLayout"
import TableHeader from "components/table/TableHeader"
import GraphError from "components/utils/GraphError"
import { GetEdges, GetEdgesVariables } from "./__generated__/GetEdges"

export const GET_EDGES = gql`
  query GetEdges($organisationName: String!, $workspaceName: String!) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      edges {
        data {
          id
          namespace
          name
          display_name
          is_active
          data_source
          metadata
          source {
            id
            namespace
            name
            display_name
          }
          destination {
            id
            namespace
            name
            display_name
          }
        }
        meta {
          total
        }
      }
    }
  }
`

const Edges: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()
  const [search, setSearch] = useState<string>()

  const { loading, error, data, refetch } = useQuery<
    GetEdges,
    GetEdgesVariables
  >(GET_EDGES, {
    variables: {
      organisationName,
      workspaceName,
    },
  })

  if (error) return <GraphError error={error} />

  const edges = data?.workspace?.edges.data ?? []

  const handleRefresh = () => refetch()

  const filteredEdges = search
    ? edges.filter(edge =>
        edge.name.toLowerCase().includes(search.toLowerCase())
      )
    : edges

  return (
    <PageLayout>
      <PageHeader title="Edges" />
      <PageContent>
        <TableHeader
          search={search}
          onSearch={setSearch}
          onRefresh={handleRefresh}
        />
        <EdgesTable
          edges={filteredEdges}
          loading={loading}
          total={data?.workspace.edges.meta.total ?? 0}
        />
      </PageContent>
    </PageLayout>
  )
}

export default Edges
