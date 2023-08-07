import React from "react"
import { gql, useMutation } from "@apollo/client"
import { useSnackbar } from "notistack"
import { useNavigate } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"
import FilterForm, { Values } from "components/filters/FilterForm"
import GraphError from "components/utils/GraphError"
import {
  CreateFilter as CreateFilterType,
  CreateFilterVariables,
} from "./__generated__/CreateFilter"
import { NewFilter } from "./__generated__/NewFilter"
import { Source } from "./FilterRow"

export const CREATE_FILTER = gql`
  mutation CreateFilter($workspaceId: ID!, $name: String!, $metadata: JSON!) {
    createFilter(workspaceId: $workspaceId, name: $name, metadata: $metadata) {
      id
      name
      metadata
      created_at
    }
  }
`

type CreateFilterProps = {
  workspaceId: string
  namespaces: string[]
  tags: string[]
  sources: Source[]
}

const CreateFilter: React.FC<CreateFilterProps> = ({
  workspaceId,
  namespaces,
  tags,
  sources,
}) => {
  const { routePrefix } = useWorkspace()
  const { enqueueSnackbar } = useSnackbar()
  const navigate = useNavigate()

  /* istanbul ignore next */
  const [createFilter, { loading, error }] = useMutation<
    CreateFilterType,
    CreateFilterVariables
  >(CREATE_FILTER, {
    update(cache, { data }) {
      cache.modify({
        id: cache.identify({
          id: workspaceId,
          __typename: "Workspace",
        }),
        fields: {
          filters(existingFilters = { data: [] }) {
            if (!data?.createFilter) return

            const newFilter = cache.writeFragment<NewFilter>({
              data: data.createFilter,
              fragment: gql`
                fragment NewFilter on Filter {
                  id
                  name
                  metadata
                  created_at
                }
              `,
            })
            return {
              data: [...existingFilters.data, newFilter],
              meta: {
                total: (existingFilters.meta?.total ?? 0) + 1,
                __typename: "FilterPagination",
              },
            }
          },
        },
      })
    },
  })

  const handleSave = (values: Values) =>
    createFilter({
      variables: {
        workspaceId,
        ...values,
      },
    })
      .then(data =>
        navigate(`${routePrefix}/filters/${data.data?.createFilter.id}`),
      )
      .then(() => enqueueSnackbar("Filter created", { variant: "success" }))
      .catch(() => {})

  return (
    <>
      {error && <GraphError error={error} />}
      <FilterForm
        onSave={handleSave}
        loading={loading}
        namespaces={namespaces}
        tags={tags}
        sources={sources}
      />
    </>
  )
}

export default CreateFilter
