import React from "react"
import { gql, useQuery } from "@apollo/client"
import { FilterAlt } from "@mui/icons-material"
import {
  Autocomplete,
  CircularProgress,
  InputAdornment,
  TextField,
} from "@mui/material"
import useSearchParams from "helpers/useSearchParams"
import useWorkspace from "helpers/useWorkspace"
import GraphError from "components/utils/GraphError"
import {
  GetFiltersControl,
  GetFiltersControlVariables,
} from "./__generated__/GetFiltersControl"

export const GET_FILTERS = gql`
  query GetFiltersControl($organisationName: String!, $workspaceName: String!) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      filters {
        data {
          id
          name
        }
      }
    }
  }
`

type Option = {
  value: string
  label: string | null
}

const FilterControl: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()
  const { searchParams, setSearchParam } = useSearchParams()

  const { loading, error, data } = useQuery<
    GetFiltersControl,
    GetFiltersControlVariables
  >(GET_FILTERS, {
    variables: {
      organisationName,
      workspaceName,
    },
  })

  const options: Option[] =
    data?.workspace?.filters?.data
      .filter(filter => filter.name)
      .map(filter => ({
        value: filter.id,
        label: filter.name,
      })) || []

  const filterId = searchParams.get("filter")

  const value = options?.find(filter => filter.value === filterId) || null

  const handleChange = (
    event: React.SyntheticEvent<Element, Event>,
    newValue: Option | null
  ) => setSearchParam("filter", newValue?.value || null)

  return (
    <>
      <Autocomplete<Option>
        options={options}
        value={value}
        onChange={handleChange}
        size="small"
        renderInput={params => (
          <TextField
            {...params}
            placeholder="Filter"
            InputProps={{
              ...params.InputProps,
              startAdornment: (
                <InputAdornment position="start">
                  <FilterAlt />
                </InputAdornment>
              ),
              endAdornment: loading ? (
                <InputAdornment position="end">
                  <CircularProgress />
                </InputAdornment>
              ) : (
                params.InputProps.endAdornment
              ),
            }}
          />
        )}
        data-testid="filter-control"
        sx={{ backgroundColor: "white", width: 250 }}
      />
      {error && <GraphError error={error} />}
    </>
  )
}

export default FilterControl
