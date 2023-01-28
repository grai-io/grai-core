import React, { useState } from "react"
import { gql, useQuery } from "@apollo/client"
import TablesHeader from "components/tables/TablesHeader"
import { useParams } from "react-router-dom"
import { Box } from "@mui/material"
import GraphError from "components/utils/GraphError"
import PageLayout from "components/layout/PageLayout"
import { GetTables, GetTablesVariables } from "./__generated__/GetTables"
import TablesTable from "components/tables/TablesTable"

export const GET_TABLES = gql`
  query GetTables($workspaceId: ID!) {
    workspace(pk: $workspaceId) {
      id
      tables {
        id
        namespace
        name
        display_name
        is_active
        data_source
        metadata
      }
    }
  }
`

export interface Table {
  id: string
  namespace: string
  name: string
  display_name: string
  data_source: string
  is_active: boolean
}

const Tables: React.FC = () => {
  const { workspaceId } = useParams()
  const [search, setSearch] = useState<string>()

  const { loading, error, data, refetch } = useQuery<
    GetTables,
    GetTablesVariables
  >(GET_TABLES, {
    variables: {
      workspaceId: workspaceId ?? "",
    },
  })

  if (error) return <GraphError error={error} />

  const tables = data?.workspace?.tables ?? []

  const handleRefresh = () => refetch()

  const filteredTables = search
    ? tables.filter(table =>
        table.name.toLowerCase().includes(search.toLowerCase())
      )
    : tables

  return (
    <PageLayout>
      <TablesHeader
        search={search}
        onSearch={setSearch}
        onRefresh={handleRefresh}
      />
      <Box sx={{ px: 3 }}>
        <TablesTable tables={filteredTables} loading={loading} />
      </Box>
    </PageLayout>
  )
}

export default Tables
