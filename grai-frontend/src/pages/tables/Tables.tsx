import React, { useState } from "react"
import { gql, useQuery } from "@apollo/client"
import useWorkspace from "helpers/useWorkspace"
import PageContent from "components/layout/PageContent"
import PageHeader from "components/layout/PageHeader"
import PageLayout from "components/layout/PageLayout"
import TableHeader from "components/table/TableHeader"
import TablesTable from "components/tables/TablesTable"
import GraphError from "components/utils/GraphError"
import { GetTables, GetTablesVariables } from "./__generated__/GetTables"

export const GET_TABLES = gql`
  query GetTables(
    $organisationName: String!
    $workspaceName: String!
    $offset: Int
    $search: String
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      tables(pagination: { limit: 20, offset: $offset }, search: $search) {
        data {
          id
          namespace
          name
          display_name
          is_active
          data_source
          metadata
        }
        meta {
          filtered
          total
        }
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
  const [page, setPage] = useState<number>(0)

  const { loading, error, data, refetch } = useQuery<
    GetTables,
    GetTablesVariables
  >(GET_TABLES, {
    variables: {
      organisationName,
      workspaceName,
      offset: page * 20,
      search,
    },
    context: {
      debounceKey: "tables",
      debounceTimeout: 1000,
    },
  })

  if (error) return <GraphError error={error} />

  const tables = data?.workspace?.tables.data ?? []

  const handleRefresh = () => refetch()
  const handleSearch = (value: string) => {
    setSearch(value)
    setPage(0)
  }

  return (
    <PageLayout>
      <PageHeader title="Tables" />
      <PageContent>
        <TableHeader
          search={search}
          onSearch={handleSearch}
          onRefresh={handleRefresh}
        />
        <TablesTable
          tables={tables}
          loading={loading}
          total={data?.workspace.tables.meta.filtered ?? 0}
          page={page}
          onPageChange={setPage}
        />
      </PageContent>
    </PageLayout>
  )
}

export default Tables
