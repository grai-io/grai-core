import React from "react"
import { gql, useMutation } from "@apollo/client"
import { Dialog, DialogContent } from "@mui/material"
import { useSnackbar } from "notistack"
import DialogTitle from "components/dialogs/DialogTitle"
import GraphError from "components/utils/GraphError"
import {
  UpdateMembership,
  UpdateMembershipVariables,
} from "./__generated__/UpdateMembership"
import EditMembershipForm, {
  Membership,
  Values,
} from "./forms/EditMembershipForm"

export const UPDATE_MEMBERSHIP = gql`
  mutation UpdateMembership($id: ID!, $role: String!, $is_active: Boolean!) {
    updateMembership(id: $id, role: $role, is_active: $is_active) {
      id
      role
      is_active
    }
  }
`

type EditMembershipDialogProps = {
  membership: Membership
  open: boolean
  onClose: () => void
}

const EditMembershipDialog: React.FC<EditMembershipDialogProps> = ({
  membership,
  open,
  onClose,
}) => {
  const { enqueueSnackbar } = useSnackbar()

  const [updateMembership, { loading, error }] = useMutation<
    UpdateMembership,
    UpdateMembershipVariables
  >(UPDATE_MEMBERSHIP)

  const handleSubmit = (values: Values) =>
    updateMembership({
      variables: {
        id: membership.id,
        role: values.role,
        is_active: values.is_active,
      },
    })
      .then(() => onClose())
      .then(() => enqueueSnackbar("Membership updated"))
      .catch(err => {})

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle onClose={onClose}>Edit Membership</DialogTitle>
      <DialogContent>
        {error && <GraphError error={error} />}
        <EditMembershipForm
          membership={membership}
          onSubmit={handleSubmit}
          loading={loading}
        />
      </DialogContent>
    </Dialog>
  )
}

export default EditMembershipDialog
