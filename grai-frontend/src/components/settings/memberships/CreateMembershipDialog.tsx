import { gql, useMutation } from "@apollo/client"
import { Dialog, DialogContent } from "@mui/material"
import React from "react"
import { useParams } from "react-router-dom"
import DialogTitle from "components/dialogs/DialogTitle"
import CreateKeyForm, { Values } from "./CreateMembershipForm"
import GraphError from "components/utils/GraphError"
import {
  CreateMembership,
  CreateMembershipVariables,
} from "./__generated__/CreateMembership"
import { useSnackbar } from "notistack"

export const CREATE_MEMBERSHIP = gql`
  mutation CreateMembership(
    $role: String!
    $email: String!
    $workspaceId: ID!
  ) {
    createMembership(role: $role, email: $email, workspaceId: $workspaceId) {
      id
      role
      user {
        id
        username
      }
    }
  }
`

type CreateKeyDialogProps = {
  open: boolean
  onClose: () => void
}

const CreateKeyDialog: React.FC<CreateKeyDialogProps> = ({ open, onClose }) => {
  const { workspaceId } = useParams()
  const { enqueueSnackbar } = useSnackbar()

  const [createMembership, { loading, error }] = useMutation<
    CreateMembership,
    CreateMembershipVariables
  >(CREATE_MEMBERSHIP)

  const handleSubmit = (values: Values) =>
    createMembership({
      variables: {
        ...values,
        workspaceId: workspaceId ?? "",
      },
    })
      .then(() => onClose())
      .then(() => enqueueSnackbar("Membership added"))
      .catch(err => {})

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle onClose={onClose}>Invite user</DialogTitle>
      <DialogContent>
        {error && <GraphError error={error} />}
        <CreateKeyForm onSubmit={handleSubmit} loading={loading} />
      </DialogContent>
    </Dialog>
  )
}

export default CreateKeyDialog
