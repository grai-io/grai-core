import React from "react"
import { gql, useMutation } from "@apollo/client"
import { Delete } from "@mui/icons-material"
import { MenuItem, ListItemIcon, ListItemText } from "@mui/material"
import { useConfirm } from "material-ui-confirm"
import { useSnackbar } from "notistack"
import {
  DeleteConnection,
  DeleteConnectionVariables,
} from "./__generated__/DeleteConnection"

export const DELETE_CONNECTION = gql`
  mutation DeleteConnection($id: ID!) {
    deleteConnection(id: $id) {
      id
    }
  }
`

export interface Connection {
  id: string
  name: string
}

type ConnectionDeleteProps = {
  connection: Connection
  workspaceId?: string
  onClose: () => void
  onDelete?: () => void
}

const ConnectionDelete: React.FC<ConnectionDeleteProps> = ({
  connection,
  workspaceId,
  onClose,
  onDelete,
}) => {
  const confirm = useConfirm()
  const { enqueueSnackbar } = useSnackbar()

  /* istanbul ignore next */
  const [deleteConnection] = useMutation<
    DeleteConnection,
    DeleteConnectionVariables
  >(DELETE_CONNECTION, {
    variables: { id: connection.id },
    update(cache, { data }) {
      cache.modify({
        id: cache.identify({
          id: workspaceId,
          __typename: "Workspace",
        }),
        fields: {
          connections: (existingConnections = { data: [] }, { readField }) => ({
            data: existingConnections.data
              ? existingConnections.data.filter(
                  (keyRef: any) =>
                    data?.deleteConnection.id !== readField("id", keyRef),
                )
              : [],
          }),
        },
      })
    },
  })

  const handleDelete = () => {
    onClose()
    confirm({
      title: "Delete Connection",
      description: `Are you sure you wish to delete the ${connection.name} connection?`,
      confirmationText: "Delete",
    })
      .then(() => deleteConnection())
      .then(() => enqueueSnackbar("Connection deleted", { variant: "success" }))
      .then(onDelete)
      .catch(
        error =>
          error &&
          enqueueSnackbar(`Failed to delete connection ${error}`, {
            variant: "error",
          }),
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

export default ConnectionDelete
