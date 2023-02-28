import React, { useState } from "react"
import { gql, useQuery } from "@apollo/client"
import { Box } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import PageLayout from "components/layout/PageLayout"
import TablesHeader from "components/tables/TablesHeader"
import TablesTable from "components/tables/TablesTable"
import GraphError from "components/utils/GraphError"
import { GetTables, GetTablesVariables } from "./__generated__/GetTables"

export const GET_TABLES = gql`
  query GetTables($organisationName: String!, $workspaceName: String!) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
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
  const { organisationName, workspaceName } = useWorkspace()
  const [search, setSearch] = useState<string>()

  const { loading, error, data, refetch } = useQuery<
    GetTables,
    GetTablesVariables
  >(GET_TABLES, {
    variables: {
      organisationName,
      workspaceName,
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
