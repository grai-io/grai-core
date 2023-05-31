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
  query GetEdges(
    $organisationName: String!
    $workspaceName: String!
    $offset: Int
    $search: String
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      edges(pagination: { limit: 20, offset: $offset }, search: $search) {
        data {
          id
          namespace
          name
          display_name
          is_active
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
          filtered
          total
        }
      }
    }
  }
`

const Edges: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()
  const [search, setSearch] = useState<string>()
  const [page, setPage] = useState<number>(0)

  const { loading, error, data, refetch } = useQuery<
    GetEdges,
    GetEdgesVariables
  >(GET_EDGES, {
    variables: {
      organisationName,
      workspaceName,
      offset: page * 20,
      search,
    },
    context: {
      debounceKey: "edges",
      debounceTimeout: 1000,
    },
  })

  if (error) return <GraphError error={error} />

  const edges = data?.workspace?.edges.data ?? []

  const handleRefresh = () => refetch()

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
          edges={edges}
          loading={loading}
          total={data?.workspace.edges.meta.filtered ?? 0}
          page={page}
          onPageChange={setPage}
        />
      </PageContent>
    </PageLayout>
  )
}

export default Edges
