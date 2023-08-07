import React from "react"
import { gql, useMutation } from "@apollo/client"
import { useSnackbar } from "notistack"
import FilterForm, { Values } from "components/filters/FilterForm"
import GraphError from "components/utils/GraphError"
import {
  UpdateFilter as UpdateFilterType,
  UpdateFilterVariables,
} from "./__generated__/UpdateFilter"
import { Filter as FilterType, Source } from "./FilterRow"

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
  namespaces: string[]
  tags: string[]
  sources: Source[]
  workspaceId: string
}

const UpdateFilter: React.FC<UpdateFilterProps> = ({
  filter,
  namespaces,
  tags,
  sources,
  workspaceId,
}) => {
  const { enqueueSnackbar } = useSnackbar()

  const [updateFilter, { loading, error }] = useMutation<
    UpdateFilterType,
    UpdateFilterVariables
  >(UPDATE_FILTER, {
    update(cache) {
      cache.evict({
        id: cache.identify({
          id: workspaceId,
          __typename: "Workspace",
        }),
        fieldName: "tables",
      })
    },
  })

  const handleSave = (values: Values) =>
    updateFilter({ variables: { id: filter.id, ...values } })
      .then(() => enqueueSnackbar("Filter updated"))
      .catch(() => {})

  return (
    <>
      {error && <GraphError error={error} />}
      <FilterForm
        defaultValues={{
          name: filter.name ?? "",
          metadata: filter.metadata,
        }}
        onSave={handleSave}
        loading={loading}
        namespaces={namespaces}
        tags={tags}
        sources={sources}
      />
    </>
  )
}

export default UpdateFilter
