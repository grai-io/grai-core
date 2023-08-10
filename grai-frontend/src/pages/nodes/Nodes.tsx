import React, { useState } from "react"
import { gql, useQuery } from "@apollo/client"
import useWorkspace from "helpers/useWorkspace"
import PageContent from "components/layout/PageContent"
import PageHeader from "components/layout/PageHeader"
import PageLayout from "components/layout/PageLayout"
import NodeHeader from "components/nodes/NodeHeader"
import NodesTable from "components/nodes/NodesTable"
import GraphError from "components/utils/GraphError"
import { GetNodes, GetNodesVariables } from "./__generated__/GetNodes"

export const GET_NODES = gql`
  query GetNodes(
    $organisationName: String!
    $workspaceName: String!
    $offset: Int
    $search: String
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      nodes(pagination: { limit: 20, offset: $offset }, search: $search) {
        data {
          id
          namespace
          name
          display_name
          is_active
          metadata
          data_sources {
            data {
              id
              name
              connections {
                data {
                  id
                  connector {
                    id
                    name
                    slug
                  }
                }
              }
            }
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

const Nodes: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()
  const [search, setSearch] = useState<string>()
  const [page, setPage] = useState<number>(0)

  const { loading, error, data, refetch } = useQuery<
    GetNodes,
    GetNodesVariables
  >(GET_NODES, {
    variables: {
      organisationName,
      workspaceName,
      offset: page * 20,
      search,
    },
    context: {
      debounceKey: "nodes",
      debounceTimeout: 1000,
    },
  })

  if (error) return <GraphError error={error} />

  const nodes = data?.workspace?.nodes.data ?? []

  const handleRefresh = () => refetch()
  const handleSearch = (value: string) => {
    setSearch(value)
    setPage(0)
  }

  return (
    <PageLayout>
      <PageHeader title="Nodes" />
      <PageContent>
        <NodeHeader
          search={search}
          onSearch={handleSearch}
          onRefresh={handleRefresh}
        />
        <NodesTable
          nodes={nodes}
          loading={loading}
          total={data?.workspace.nodes.meta.filtered ?? 0}
          page={page}
          onPageChange={setPage}
        />
      </PageContent>
    </PageLayout>
  )
}

export default Nodes
