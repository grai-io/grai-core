import React, { useState } from "react"
import { gql, useQuery } from "@apollo/client"
import { Typography } from "@mui/material"
import TableHeader from "components/nodes/NodeHeader"
import GraphError from "components/utils/GraphError"
import {
  GetSourceTables,
  GetSourceTablesVariables,
} from "./__generated__/GetSourceTables"
import SourceTablesTable from "./SourceTablesTable"

export const GET_SOURCE_TABLES = gql`
  query GetSourceTables(
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
          filters: { node_type: "Table" }
          pagination: { limit: 20, offset: $offset }
          search: $search
        ) {
          data {
            id
            namespace
            name
            display_name
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

type SourceTablesProps = {
  source: Source
  workspaceId: string
}

const SourceTables: React.FC<SourceTablesProps> = ({ source, workspaceId }) => {
  const [search, setSearch] = useState<string | null>(null)
  const [page, setPage] = useState<number>(0)

  const { loading, error, data, refetch } = useQuery<
    GetSourceTables,
    GetSourceTablesVariables
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

  const tables = data?.workspace?.source?.nodes.data ?? []

  if (tables.length === 0 && !search && !loading) {
    return (
      <Typography sx={{ textAlign: "center", p: 5 }}>
        No tables found
      </Typography>
    )
  }

  return (
    <>
      <TableHeader
        search={search}
        onSearch={handleSearch}
        onRefresh={handleRefresh}
      />
      <SourceTablesTable
        tables={tables}
        total={data?.workspace?.source?.nodes.meta.filtered ?? 0}
        page={page}
        onPageChange={setPage}
        loading={loading}
      />
    </>
  )
}

export default SourceTables
