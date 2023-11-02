import React, { useEffect } from "react"
import { gql, useQuery } from "@apollo/client"
import { useSnackbar } from "notistack"
import useWorkspace from "helpers/useWorkspace"
import {
  GetFiltersControl,
  GetFiltersControlVariables,
} from "./__generated__/GetFiltersControl"
import FilterMenu from "./filters/FilterMenu"

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

  return <FilterMenu options={options} />
}

export default FilterControl
