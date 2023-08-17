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

export const GET_WORKSPACE = gql`
  query GetWorkspaceFilterInline($workspaceId: ID!) {
    workspace(id: $workspaceId) {
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
  workspaceId: string
}

const GraphFilterInline: React.FC<GraphFilterInlineProps> = ({
  workspaceId,
}) => {
  const [filter, setFilter] = React.useState<Filter>(defaultFilter)

  const { loading, error, data } = useQuery<
    GetWorkspaceFilterInline,
    GetWorkspaceFilterInlineVariables
  >(GET_WORKSPACE, {
    variables: {
      workspaceId,
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

  return (
    <Box sx={{ p: 1 }}>
      <FilterField<Property>
        options={properties}
        // value={property}
        // onChange={(event, newValue) =>
        //   onChange({ ...filter, type: newValue?.value ?? null })
        // }
        data-testid="autocomplete-property"
        size="small"
      />
      <FilterField<Field>
        disabled={!property}
        options={property?.fields ?? []}
        value={field}
        onChange={handleFieldChange}
        data-testid="autocomplete-field"
        size="small"
      />
      <FilterField<Operator>
        disabled={!field}
        options={field?.operators ?? []}
        value={operator}
        onChange={(event, newValue) =>
          setFilter({ ...filter, operator: newValue?.value ?? null })
        }
        data-testid="autocomplete-operator"
        size="small"
      />
      {operator?.valueComponent ? (
        operator.valueComponent(
          !operator,
          filter.value,
          (value: string | string[] | null) => setFilter({ ...filter, value }),
        )
      ) : (
        <TextField
          fullWidth
          disabled={!operator}
          value={filter.value ?? ""}
          onChange={event =>
            setFilter({ ...filter, value: event.target.value })
          }
          inputProps={{
            "data-testid": "value",
          }}
          size="small"
        />
      )}
    </Box>
  )
}

export default GraphFilterInline
