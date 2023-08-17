import { gql, useQuery } from "@apollo/client"
import { Box, CircularProgress, TextField } from "@mui/material"
import FilterField from "components/filters/FilterField"
import {
  Field,
  Filter,
  Operator,
  Property,
  defaultFilter,
  getProperties,
} from "components/filters/filters"
import GraphError from "components/utils/GraphError"
import React from "react"
import {
  GetWorkspaceFilterInline,
  GetWorkspaceFilterInlineVariables,
} from "./__generated__/GetWorkspaceFilterInline"
import GraphFilterTextbox from "./GraphFilterTextbox"
import useWorkspace from "helpers/useWorkspace"

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

const GraphFilterInline: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()
  const [filter, setFilter] = React.useState<Filter>(defaultFilter)

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

  const property =
    properties.find(property => property.value === filter.type) ?? null
  const field =
    property?.fields.find(field => field.value === filter.field) ?? null
  const operator =
    field?.operators.find(operator => operator.value === filter.operator) ??
    null

  const handleFieldChange = (
    _: React.SyntheticEvent<Element, Event>,
    newValue: Field | null,
  ) => {
    let newFilter = { ...filter, field: newValue?.value ?? null }

    if (!operator && newValue?.operators && newValue?.operators.length > 0) {
      newFilter.operator = newValue?.operators[0].value
    }

    setFilter(newFilter)
  }

  return <GraphFilterTextbox />
}

export default GraphFilterInline
