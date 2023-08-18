import { gql, useQuery } from "@apollo/client"
import { Box, Button, CircularProgress, Stack } from "@mui/material"
import {
  Filter,
  defaultFilter,
  getProperties,
} from "components/filters/filters"
import GraphError from "components/utils/GraphError"
import React from "react"
import {
  GetWorkspaceFilterInline,
  GetWorkspaceFilterInlineVariables,
} from "./__generated__/GetWorkspaceFilterInline"
import useWorkspace from "helpers/useWorkspace"
import { Add, Save } from "@mui/icons-material"
import FilterRow from "./filters-inline/FilterRow"

export const GET_WORKSPACE = gql`
  query GetWorkspaceFilterInline(
    $organisationName: String!
    $workspaceName: String!
  ) {
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
    }
  }
`
type GraphFilterInlineProps = {
  inlineFilters: Filter[]
  setInlineFilters: (filters: Filter[]) => void
}

const GraphFilterInline: React.FC<GraphFilterInlineProps> = ({
  inlineFilters,
  setInlineFilters,
}) => {
  const { organisationName, workspaceName } = useWorkspace()

  const { loading, error, data } = useQuery<
    GetWorkspaceFilterInline,
    GetWorkspaceFilterInlineVariables
  >(GET_WORKSPACE, {
    variables: {
      organisationName,
      workspaceName,
    },
  })

  if (loading) return <CircularProgress />
  if (error) return <GraphError error={error} />

  const workspace = data?.workspace

  if (!workspace) return null

  const properties = getProperties(
    workspace.namespaces.data,
    workspace.tags.data,
    workspace.sources.data,
  )

  const handleFilterChange = (index: number) => (filter: Filter) => {
    const newFilters = [...inlineFilters]
    newFilters[index] = filter
    setInlineFilters(newFilters)
  }

  const handleFilterDelete = (index: number) => () => {
    const newFilters = [...inlineFilters]
    newFilters.splice(index, 1)
    setInlineFilters(newFilters)
  }

  const handleAddField = () =>
    setInlineFilters([
      ...inlineFilters,
      {
        ...defaultFilter,
        field: properties[0].fields[0].value,
        operator: properties[0].fields[0].operators[0].value,
      },
    ])

  return (
    <Box sx={{ p: 1 }}>
      <Stack direction="row" spacing={1} sx={{ mb: 1 }}>
        <Button
          variant="outlined"
          fullWidth
          startIcon={<Add />}
          onClick={handleAddField}
        >
          Add Field
        </Button>
        <Button variant="outlined" fullWidth startIcon={<Save />}>
          Save
        </Button>
      </Stack>
      {inlineFilters.map((filter, index) => (
        <FilterRow
          properties={properties}
          filter={filter}
          setFilter={handleFilterChange(index)}
          onDelete={handleFilterDelete(index)}
        />
      ))}
    </Box>
  )
}

export default GraphFilterInline
