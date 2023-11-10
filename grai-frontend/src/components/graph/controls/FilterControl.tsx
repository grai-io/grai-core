import React, { useEffect } from "react"
import { gql, useQuery } from "@apollo/client"
import { useSnackbar } from "notistack"
import useWorkspace from "helpers/useWorkspace"
import {
  GetFiltersControl,
  GetFiltersControlVariables,
} from "./__generated__/GetFiltersControl"
import FilterMenu from "./filters/FilterMenu"
import { CombinedFilters } from "../useCombinedFilters"

export const GET_FILTERS = gql`
  query GetFiltersControl($organisationName: String!, $workspaceName: String!) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      name
      namespaces {
        data
      }
      tags {
        data
      }
      sources {
        data {
          id
          name
        }
      }
      filters {
        data {
          id
          name
        }
      }
    }
  }
`

export type Values = {
  namespaces: string[]
  tags: string[]
  sources: {
    id: string
    name: string
  }[]
}

type Option = {
  value: string
  label: string | null
}

type FilterControlProps = {
  combinedFilters: CombinedFilters
}

const FilterControl: React.FC<FilterControlProps> = ({ combinedFilters }) => {
  const { enqueueSnackbar } = useSnackbar()
  const { organisationName, workspaceName } = useWorkspace()

  const { error, data } = useQuery<
    GetFiltersControl,
    GetFiltersControlVariables
  >(GET_FILTERS, {
    variables: {
      organisationName,
      workspaceName,
    },
  })

  useEffect(() => {
    error &&
      enqueueSnackbar(error.message, {
        variant: "error",
      })
  }, [error, enqueueSnackbar])

  const options: Option[] =
    data?.workspace?.filters?.data
      .filter(filter => filter.name)
      .map(filter => ({
        value: filter.id,
        label: filter.name,
      })) || []

  const values: Values = {
    namespaces: data?.workspace.namespaces.data || [],
    tags: data?.workspace.tags.data || [],
    sources: data?.workspace.sources.data || [],
  }

  return (
    <FilterMenu
      options={options}
      combinedFilters={combinedFilters}
      values={values}
      workspaceId={data?.workspace.id}
    />
  )
}

export default FilterControl
