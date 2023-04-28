import React from "react"
import { gql, useMutation } from "@apollo/client"
import { Delete } from "@mui/icons-material"
import { MenuItem, ListItemIcon, ListItemText } from "@mui/material"
import { useConfirm } from "material-ui-confirm"
import { useSnackbar } from "notistack"
import {
  DeleteFilter,
  DeleteFilterVariables,
} from "./__generated__/DeleteFilter"

export const DELETE_FILTER = gql`
  mutation DeleteFilter($id: ID!) {
    deleteFilter(id: $id) {
      id
    }
  }
`

export interface Filter {
  id: string
  name: string | null
}

type FilterDeleteProps = {
  filter: Filter
  workspaceId?: string
  onClose: (deleted: boolean) => void
}

const FilterDelete: React.FC<FilterDeleteProps> = ({
  filter,
  workspaceId,
  onClose,
}) => {
  const confirm = useConfirm()
  const { enqueueSnackbar } = useSnackbar()

  const [deleteFilter] = useMutation<DeleteFilter, DeleteFilterVariables>(
    DELETE_FILTER,
    {
      variables: { id: filter.id },
      update(cache, { data }) {
        cache.modify({
          id: cache.identify({
            id: workspaceId,
            __typename: "Workspace",
          }),
          fields: {
            filters: (existingFilters = { data: [] }, { readField }) => ({
              data: existingFilters.data.filter(
                (keyRef: any) =>
                  data?.deleteFilter.id !== readField("id", keyRef)
              ),
            }),
          },
        })
      },
    }
  )

  const handleDelete = () => {
    onClose(true)
    confirm({
      title: "Delete Filter",
      description: `Are you sure you wish to delete the ${filter.name} filter?`,
      confirmationText: "Delete",
    })
      .then(() => deleteFilter())
      .then(() => enqueueSnackbar("Filter deleted", { variant: "success" }))
      .catch(() => {})
  }

  return (
    <MenuItem onClick={handleDelete}>
      <ListItemIcon>
        <Delete />
      </ListItemIcon>
      <ListItemText primary="Delete" />
    </MenuItem>
  )
}

export default FilterDelete
