import React from "react"
import { gql, useMutation } from "@apollo/client"
import { Box } from "@mui/material"
import { useSnackbar } from "notistack"
import FilterForm, { Values } from "components/filters/FilterForm"
import GraphError from "components/utils/GraphError"
import {
  UpdateFilter as UpdateFilterType,
  UpdateFilterVariables,
} from "./__generated__/UpdateFilter"
import { Filter as FilterType } from "./FilterRow"

export const UPDATE_FILTER = gql`
  mutation UpdateFilter($id: ID!, $name: String!, $metadata: JSON!) {
    updateFilter(id: $id, name: $name, metadata: $metadata) {
      id
      name
      metadata
      created_at
    }
  }
`

interface Filter {
  id: string
  name: string | null
  metadata: FilterType[]
}

type UpdateFilterProps = {
  filter: Filter
}

const UpdateFilter: React.FC<UpdateFilterProps> = ({ filter }) => {
  const { enqueueSnackbar } = useSnackbar()

  const [updateFilter, { loading, error }] = useMutation<
    UpdateFilterType,
    UpdateFilterVariables
  >(UPDATE_FILTER)

  const handleSave = (values: Values) =>
    updateFilter({ variables: { id: filter.id, ...values } })
      .then(() => enqueueSnackbar("Filter updated"))
      .catch(() => {})

  return (
    <Box sx={{ p: 3 }}>
      {error && <GraphError error={error} />}
      <FilterForm
        defaultValues={{
          name: filter.name ?? "",
          metadata: filter.metadata,
        }}
        onSave={handleSave}
        loading={loading}
      />
    </Box>
  )
}

export default UpdateFilter
