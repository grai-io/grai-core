import React from "react"
import { gql, useMutation } from "@apollo/client"
import { Dialog, DialogContent } from "@mui/material"
import DialogTitle from "components/dialogs/DialogTitle"
import { NewFilter } from "components/filters/__generated__/NewFilter"
import { Filter } from "components/filters/filters"
import GraphError from "components/utils/GraphError"
import {
  CreateFilterInline,
  CreateFilterInlineVariables,
} from "./__generated__/CreateFilterInline"
import CreateFilterForm, { Values } from "./CreateFilterForm"
import { useSnackbar } from "notistack"

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

type SaveDialogProps = {
  workspaceId: string
  inlineFilters: Filter[]
  open: boolean
  onClose: () => void
}

const SaveDialog: React.FC<SaveDialogProps> = ({
  workspaceId,
  inlineFilters,
  open,
  onClose,
}) => {
  const { enqueueSnackbar } = useSnackbar()

  /* istanbul ignore next */
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
      variables: { workspaceId, metadata: inlineFilters, ...values },
    })
      .then(() => enqueueSnackbar("Filter created", { variant: "success" }))
      .then(onClose)
      .catch(() => {})

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle onClose={onClose}>Save Filter</DialogTitle>
      <DialogContent>
        {error && <GraphError error={error} />}
        <CreateFilterForm onSubmit={handleSave} loading={loading} />
      </DialogContent>
    </Dialog>
  )
}

export default SaveDialog
