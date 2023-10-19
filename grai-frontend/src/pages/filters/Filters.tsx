import React, { useState } from "react"
import { gql, useQuery } from "@apollo/client"
import { Add } from "@mui/icons-material"
import { Button } from "@mui/material"
import { Link } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"
import FiltersTable from "components/filters/FiltersTable"
import PageContent from "components/layout/PageContent"
import PageHeader from "components/layout/PageHeader"
import TableHeader from "components/table/TableHeader"
import GraphError from "components/utils/GraphError"
import { GetFilters, GetFiltersVariables } from "./__generated__/GetFilters"

export const GET_FILTERS = gql`
  query GetFilters($organisationName: String!, $workspaceName: String!) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      filters {
        data {
          id
          name
          created_at
          created_by {
            id
            username
            first_name
            last_name
          }
        }
        meta {
          total
        }
      }
    }
  }
`

const Filters: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()
  const [search, setSearch] = useState<string>()

  const { loading, error, data, refetch } = useQuery<
    GetFilters,
    GetFiltersVariables
  >(GET_FILTERS, {
    variables: {
      organisationName,
      workspaceName,
    },
  })

  const handleRefresh = () => refetch()

  if (error) return <GraphError error={error} />

  const filters = data?.workspace?.filters.data ?? []

  const filteredFilters = search
    ? filters.filter(
        filter =>
          filter.name &&
          filter.name.toLowerCase().includes(search.toLowerCase()),
      )
    : filters

  return (
    <>
      <PageHeader
        title="Filters"
        buttons={
          <Button
            variant="contained"
            startIcon={<Add />}
            component={Link}
            to="create"
            sx={{
              backgroundColor: "#FC6016",
              boxShadow: "0px 4px 6px rgba(252, 96, 22, 0.2)",
              borderRadius: "8px",
              height: "40px",
            }}
          >
            Add Filter
          </Button>
        }
      />
      <PageContent>
        <TableHeader
          search={search}
          onSearch={setSearch}
          onRefresh={handleRefresh}
        />
        <FiltersTable
          filters={filteredFilters}
          workspaceId={data?.workspace.id}
          loading={loading}
          total={data?.workspace.filters.meta.total ?? 0}
        />
      </PageContent>
    </>
  )
}

export default Filters
