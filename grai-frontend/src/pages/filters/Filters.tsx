import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Box } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import FiltersHeader from "components/filters/FiltersHeader"
import FiltersTable from "components/filters/FiltersTable"
import PageLayout from "components/layout/PageLayout"
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

  return (
    <PageLayout>
      <FiltersHeader onRefresh={handleRefresh} />
      <Box
        sx={{
          px: 3,
        }}
      >
        <FiltersTable
          filters={data?.workspace.filters.data ?? []}
          workspaceId={data?.workspace.id}
          loading={loading}
          total={data?.workspace.filters.meta.total ?? 0}
        />
      </Box>
    </PageLayout>
  )
}

export default Filters
