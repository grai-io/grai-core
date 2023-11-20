import React from "react"
import { gql, useMutation } from "@apollo/client"
import { Delete } from "@mui/icons-material"
import { MenuItem, ListItemIcon, ListItemText } from "@mui/material"
import { useConfirm } from "material-ui-confirm"
import { useSnackbar } from "notistack"
import { DeleteAlert, DeleteAlertVariables } from "./__generated__/DeleteAlert"

export const DELETE_ALERT = gql`
  mutation DeleteAlert($id: ID!) {
    deleteAlert(id: $id) {
      id
    }
  }
`

export interface Alert {
  id: string
  name: string
}

type AlertDeleteProps = {
  alert: Alert
  workspaceId?: string
  onClose: () => void
}

const AlertDelete: React.FC<AlertDeleteProps> = ({
  alert,
  workspaceId,
  onClose,
}) => {
  const confirm = useConfirm()
  const { enqueueSnackbar } = useSnackbar()

  const [deleteAlert] = useMutation<DeleteAlert, DeleteAlertVariables>(
    DELETE_ALERT,
    {
      variables: { id: alert.id },
      update(cache, { data }) {
        cache.modify({
          id: cache.identify({
            id: workspaceId,
            __typename: "Workspace",
          }),
          fields: {
            alerts: /* istanbul ignore next */ (
              existingAlerts = { data: [] },
              { readField },
            ) =>
              existingAlerts.data.filter(
                (keyRef: any) =>
                  data?.deleteAlert.id !== readField("id", keyRef),
              ),
          },
        })
      },
    },
  )

  const handleDelete = () => {
    onClose()
    confirm({
      title: "Delete Alert",
      description: `Are you sure you wish to delete the ${alert.name} alert?`,
      confirmationText: "Delete",
    })
      .then(() => deleteAlert())
      .then(() => enqueueSnackbar("Alert deleted", { variant: "success" }))
      .catch(
        error =>
          error &&
          enqueueSnackbar(`Failed to delete alert ${error}`, {
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

export default AlertDelete
