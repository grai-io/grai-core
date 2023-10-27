import React, { useState } from "react"
import { gql, useQuery } from "@apollo/client"
import { Typography } from "@mui/material"
import TableHeader from "components/table/TableHeader"
import GraphError from "components/utils/GraphError"
import {
  GetSourceNodes,
  GetSourceNodesVariables,
} from "./__generated__/GetSourceNodes"
import SourceNodesTable from "./SourceNodesTable"

export const GET_SOURCE_TABLES = gql`
  query GetSourceNodes(
    $workspaceId: ID!
    $sourceId: ID!
    $offset: Int
    $search: String
  ) {
    workspace(id: $workspaceId) {
      id
      source(id: $sourceId) {
        id
        nodes(
          # filters: { node_type: "Table" }
          pagination: { limit: 20, offset: $offset }
          search: $search
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
          }
        }
      }
    }
  }
`

interface Source {
  id: string
}

type SourceNodesProps = {
  source: Source
  workspaceId: string
}

const SourceNodes: React.FC<SourceNodesProps> = ({ source, workspaceId }) => {
  const [search, setSearch] = useState<string | null>(null)
  const [page, setPage] = useState<number>(0)

  const { loading, error, data, refetch } = useQuery<
    GetSourceNodes,
    GetSourceNodesVariables
  >(GET_SOURCE_TABLES, {
    variables: {
      workspaceId,
      sourceId: source.id,
      offset: page * 20,
      search,
    },
    context: {
      debounceKey: "source-tables",
      debounceTimeout: 1000,
    },
  })

  const handleRefresh = () => refetch()

  const handleSearch = (value: string) => {
    setSearch(value)
    setPage(0)
  }

  if (error) return <GraphError error={error} />

  const nodes = data?.workspace?.source?.nodes.data ?? []

  if (nodes.length === 0 && !search && !loading) {
    return (
      <Typography sx={{ textAlign: "center", p: 5 }}>No nodes found</Typography>
    )
  }

  return (
    <>
      <TableHeader
        search={search}
        onSearch={handleSearch}
        onRefresh={handleRefresh}
      />
      <SourceNodesTable
        nodes={nodes}
        total={data?.workspace?.source?.nodes.meta.filtered ?? 0}
        page={page}
        onPageChange={setPage}
        loading={loading}
      />
    </>
  )
}

export default SourceNodes
