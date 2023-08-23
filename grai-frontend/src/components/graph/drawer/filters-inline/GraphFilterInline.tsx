import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Save } from "@mui/icons-material"
import { Box, Button, CircularProgress, Stack } from "@mui/material"
import NotFound from "pages/NotFound"
import useWorkspace from "helpers/useWorkspace"
import { Filter, getProperties } from "components/filters/filters"
import GraphError from "components/utils/GraphError"
import AddButton from "./AddButton"
import FilterRow from "./FilterRow"
import SaveButton from "./SaveButton"
import {
  GetWorkspaceFilterInline,
  GetWorkspaceFilterInlineVariables,
} from "../__generated__/GetWorkspaceFilterInline"

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

  if (!workspace) return <NotFound />

  const properties = getProperties(
    workspace.namespaces.data,
    workspace.tags.data,
    workspace.sources.data,
  )

  const handleAdd = (newFilter: Filter) =>
    setInlineFilters([...inlineFilters, newFilter])

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

  return (
    <Box sx={{ p: 1 }}>
      <SaveButton inlineFilters={inlineFilters} workspaceId={workspace.id} />
      {inlineFilters.map((filter, index) => (
        <FilterRow
          key={index}
          properties={properties}
          filter={filter}
          setFilter={handleFilterChange(index)}
          onDelete={handleFilterDelete(index)}
        />
      ))}
      <AddButton fields={properties[0].fields} onAdd={handleAdd} />
    </Box>
  )
}

export default GraphFilterInline
