import React, { useState } from "react"
import { gql, useQuery } from "@apollo/client"
import { useSearchParams } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"
import PageContent from "components/layout/PageContent"
import PageHeader from "components/layout/PageHeader"
import PageLayout from "components/layout/PageLayout"
import NodesTable from "components/nodes/NodesTable"
import TableFilterChoice from "components/table/TableFilterChoice"
import NodeHeader from "components/table/TableHeader"
import GraphError from "components/utils/GraphError"
import { GetNodes, GetNodesVariables } from "./__generated__/GetNodes"

export const GET_NODES = gql`
  query GetNodes(
    $organisationName: String!
    $workspaceName: String!
    $offset: Int
    $search: String
    $filter: WorkspaceNodeFilter
    $order: NodeOrder
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      nodes(
        pagination: { limit: 20, offset: $offset }
        search: $search
        filters: $filter
        order: $order
      ) {
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

type NodeFilter = {
  node_type?: {
    contains?: string[]
  }
}

interface OrderProperty {
  [key: string]: "ASC" | "DESC"
}

export type Order = {
  property: string
  direction: "asc" | "desc"
}

const Nodes: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()
  const [search, setSearch] = useState<string>()
  const [page, setPage] = useState<number>(0)
  const [order, setOrder] = useState<Order | null>(null)
  const [searchParams, setSearchParams] = useSearchParams()

  const node_types = searchParams.get("node_type")?.split(",") ?? []

  const filter: NodeFilter | undefined =
    node_types.length > 0
      ? {
          node_type: {
            contains: node_types,
          },
        }
      : undefined

  const orderProperty: OrderProperty = {}

  if (order) {
    orderProperty[order.property] = order.direction === "asc" ? "ASC" : "DESC"
  }

  const { loading, error, data, refetch } = useQuery<
    GetNodes,
    GetNodesVariables
  >(GET_NODES, {
    variables: {
      organisationName,
      workspaceName,
      offset: page * 20,
      search,
      filter,
      order: orderProperty,
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

  const handleNodeTypeChange = (value: string[]) => {
    let newParams = searchParams

    if (value.length > 0) {
      newParams.set("node_type", value.join(","))
    } else {
      newParams.delete("node_type")
    }

    setSearchParams(newParams)
  }

  return (
    <PageLayout>
      <PageHeader title="Nodes" />
      <PageContent>
        <NodeHeader
          search={search}
          onSearch={handleSearch}
          onRefresh={handleRefresh}
        >
          <TableFilterChoice
            options={["Table", "Column"]}
            placeholder="Node Type"
            value={filter?.node_type?.contains ?? []}
            onChange={handleNodeTypeChange}
          />
        </NodeHeader>
        <NodesTable
          nodes={nodes}
          loading={loading}
          total={data?.workspace.nodes.meta.filtered ?? 0}
          page={page}
          onPageChange={setPage}
          order={order}
          onOrderChange={setOrder}
        />
      </PageContent>
    </PageLayout>
  )
}

export default Nodes
