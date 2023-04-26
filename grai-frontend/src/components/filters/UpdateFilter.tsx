import React from "react"
import { gql, useMutation } from "@apollo/client"
import { Box } from "@mui/material"
import FilterForm from "components/graph/controls/filter/FilterForm"
import GraphError from "components/utils/GraphError"
import {
  UpdateFilter as UpdateFilterType,
  UpdateFilterVariables,
} from "./__generated__/UpdateFilter"
import { Filter as FilterType } from "./FilterRow"

export const UPDATE_FILTER = gql`
  mutation UpdateFilter($id: ID!, $metadata: JSON!) {
    updateFilter(id: $id, metadata: $metadata) {
      id
      name
      metadata
    }
  }
`

interface Filter {
  id: string
  metadata: FilterType[]
}

type UpdateFilterProps = {
  filter: Filter
}

const UpdateFilter: React.FC<UpdateFilterProps> = ({ filter }) => {
  const [updateFilter, { loading, error }] = useMutation<
    UpdateFilterType,
    UpdateFilterVariables
  >(UPDATE_FILTER)

  const handleSave = (filters: FilterType[]) =>
    updateFilter({ variables: { id: filter.id, metadata: filters } })

  return (
    <Box sx={{ p: 3 }}>
      {error && <GraphError error={error} />}
      <FilterForm
        defaultFilters={filter.metadata}
        onSave={handleSave}
        loading={loading}
      />
    </Box>
  )
}

export default UpdateFilter
