import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Edit, FilterAlt } from "@mui/icons-material"
import {
  Autocomplete,
  CircularProgress,
  Divider,
  IconButton,
  InputAdornment,
  TextField,
  createFilterOptions,
} from "@mui/material"
import { Link } from "react-router-dom"
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

type FilterOption =
  | Option
  | {
      menuOption: string
      label: string | null
    }
  | {
      divider: boolean
    }

const FilterControl: React.FC = () => {
  const { organisationName, workspaceName, workspaceNavigate, routePrefix } =
    useWorkspace()
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
    newValue: FilterOption | null
  ) => {
    if (!newValue) {
      setSearchParam("filter", null)
      return
    }

    if ("value" in newValue) {
      setSearchParam("filter", newValue.value)
      return
    }

    if ("menuOption" in newValue) {
      workspaceNavigate(newValue.menuOption)
      return
    }
  }

  const filter = createFilterOptions<FilterOption>()

  return (
    <>
      <Autocomplete<FilterOption>
        options={options}
        value={value}
        onChange={handleChange}
        size="small"
        filterOptions={(options, params) => {
          const filtered = filter(options, params)

          if (params.inputValue === "") {
            if (filtered.length > 0) {
              filtered.unshift({
                divider: true,
              })
            }

            filtered.unshift(
              {
                menuOption: "filters/create",
                label: "Create filter",
              },
              {
                menuOption: "filters",
                label: "Manage filters",
              }
            )
          }

          return filtered
        }}
        getOptionLabel={option => ("label" in option && option.label) || ""}
        renderOption={(props, option) =>
          "divider" in option ? (
            <Divider key="divider" sx={{ my: 1 }} />
          ) : (
            <li {...props}>{option.label}</li>
          )
        }
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
              endAdornment: (
                <>
                  {loading && (
                    <InputAdornment position="end">
                      <CircularProgress />
                    </InputAdornment>
                  )}
                  {value && (
                    <InputAdornment position="end">
                      <IconButton
                        size="small"
                        component={Link}
                        to={`${routePrefix}/filters/${value.value}`}
                        className="hello"
                        sx={{
                          visibility: "hidden",
                          mr: -1,
                        }}
                      >
                        <Edit fontSize="small" />
                      </IconButton>
                    </InputAdornment>
                  )}
                  {params.InputProps.endAdornment}
                </>
              ),
            }}
          />
        )}
        data-testid="filter-control"
        sx={{
          backgroundColor: "white",
          width: 350,
          "&.MuiAutocomplete-root:hover .hello": {
            visibility: "visible",
          },
        }}
      />
      {error && <GraphError error={error} />}
    </>
  )
}

export default FilterControl
