import React, { useState } from "react"
import { gql, useMutation } from "@apollo/client"
import { LoadingButton } from "@mui/lab"
import { Button, TextField } from "@mui/material"
import { useSnackbar } from "notistack"
import { Filter } from "components/filters/filters"
import Form from "components/form/Form"
import GraphError from "components/utils/GraphError"
import {
  CreateFilterInline,
  CreateFilterInlineVariables,
} from "./__generated__/CreateFilterInline"
import { NewFilter } from "./__generated__/NewFilter"

export const CREATE_FILTER = gql`
  mutation CreateFilterInline(
    $workspaceId: ID!
    $name: String!
    $metadata: JSON!
  ) {
    createFilter(workspaceId: $workspaceId, name: $name, metadata: $metadata) {
      id
      name
      metadata
      created_at
    }
  }
`

type Values = {
  name: string
}

type FilterSaveProps = {
  workspaceId: string
  inlineFilters: Filter[]
}

const FilterSave: React.FC<FilterSaveProps> = ({
  workspaceId,
  inlineFilters,
}) => {
  const [expanded, setExpanded] = useState(false)
  const [values, setValues] = useState<Values>({
    name: "",
  })
  const { enqueueSnackbar } = useSnackbar()

  const [createFilter, { loading, error }] = useMutation<
    CreateFilterInline,
    CreateFilterInlineVariables
  >(CREATE_FILTER, {
    update(cache, { data }) {
      cache.modify({
        id: cache.identify({
          id: workspaceId,
          __typename: "Workspace",
        }),
        fields: {
          /* istanbul ignore next */
          filters(existingFilters = { data: [] }) {
            if (!data?.createFilter) return existingFilters

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

  const handleSubmit = () =>
    createFilter({
      variables: { workspaceId, metadata: inlineFilters, ...values },
    })
      .then(() => enqueueSnackbar("Filter created", { variant: "success" }))
      .catch(() => {})

  if (expanded)
    return (
      <Form onSubmit={handleSubmit}>
        <TextField
          placeholder="Filter Name"
          size="small"
          value={values.name}
          onChange={e => setValues({ ...values, name: e.target.value })}
          InputProps={{
            sx: { borderRadius: "4px 0px 0px 4px", ml: 2 },
          }}
          inputRef={input => input && input.focus()}
          required
        />
        <LoadingButton
          variant="contained"
          type="submit"
          loading={loading}
          sx={{
            backgroundColor: "#8338EC",
            borderRadius: "0px 4px 4px 0px",
            height: "40px",
          }}
        >
          Save
        </LoadingButton>
        {error && <GraphError error={error} />}
      </Form>
    )

  const handleClick = () => setExpanded(true)

  return (
    <Button
      variant="contained"
      sx={{ backgroundColor: "#8338EC", ml: 2 }}
      onClick={handleClick}
      disabled={inlineFilters.length === 0}
    >
      Save Filter
    </Button>
  )
}

export default FilterSave
