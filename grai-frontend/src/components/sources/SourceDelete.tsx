import React from "react"
import { gql, useMutation } from "@apollo/client"
import { Delete } from "@mui/icons-material"
import { MenuItem, ListItemIcon, ListItemText } from "@mui/material"
import { useConfirm } from "material-ui-confirm"
import { useSnackbar } from "notistack"
import {
  DeleteSource,
  DeleteSourceVariables,
} from "./__generated__/DeleteSource"

export const DELETE_SOURCE = gql`
  mutation DeleteSource($id: ID!) {
    deleteSource(id: $id) {
      id
    }
  }
`

export interface Source {
  id: string
  name: string
}

type SourceDeleteProps = {
  source: Source
  workspaceId?: string
  onClose: () => void
  onDelete?: () => void
}

const SourceDelete: React.FC<SourceDeleteProps> = ({
  source,
  workspaceId,
  onClose,
  onDelete,
}) => {
  const confirm = useConfirm()
  const { enqueueSnackbar } = useSnackbar()

  const [deleteSource] = useMutation<DeleteSource, DeleteSourceVariables>(
    DELETE_SOURCE,
    {
      variables: { id: source.id },
      update(cache, { data }) {
        cache.modify({
          id: cache.identify({
            id: workspaceId,
            __typename: "Workspace",
          }),
          fields: {
            sources: (existingSources = { data: [] }, { readField }) => ({
              data: existingSources.data.filter(
                (keyRef: any) =>
                  data?.deleteSource.id !== readField("id", keyRef)
              ),
            }),
          },
        })
      },
    }
  )

  const handleDelete = () => {
    onClose()
    confirm({
      title: "Delete Source",
      description: `Are you sure you wish to delete the ${source.name} source?`,
      confirmationText: "Delete",
    })
      .then(() => deleteSource())
      .then(() => enqueueSnackbar("Source deleted", { variant: "success" }))
      .then(onDelete)
      .catch(error =>
        enqueueSnackbar(`Failed to delete source ${error}`, {
          variant: "error",
        })
      )
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

export default SourceDelete
