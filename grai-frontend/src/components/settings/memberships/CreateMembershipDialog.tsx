import React from "react"
import { gql, useMutation } from "@apollo/client"
import { Dialog, DialogContent } from "@mui/material"
import { useSnackbar } from "notistack"
import DialogTitle from "components/dialogs/DialogTitle"
import GraphError from "components/utils/GraphError"
import {
  CreateMembership,
  CreateMembershipVariables,
} from "./__generated__/CreateMembership"
import { NewMembership } from "./__generated__/NewMembership"
import CreateKeyForm, { Values } from "./CreateMembershipForm"

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
  workspaceId: string
  open: boolean
  onClose: () => void
}

const CreateKeyDialog: React.FC<CreateKeyDialogProps> = ({
  workspaceId,
  open,
  onClose,
}) => {
  const { enqueueSnackbar } = useSnackbar()

  const [createMembership, { loading, error }] = useMutation<
    CreateMembership,
    CreateMembershipVariables
  >(CREATE_MEMBERSHIP, {
    update(cache, { data }) {
      cache.modify({
        id: cache.identify({
          id: workspaceId,
          __typename: "Workspace",
        }),
        fields: {
          memberships(existingMemberships = []) {
            if (!data?.createMembership) return

            const newMembership = cache.writeFragment<NewMembership>({
              data: data.createMembership,
              fragment: gql`
                fragment NewMembership on Membership {
                  id
                  role
                  user {
                    id
                    username
                  }
                }
              `,
            })
            return [...existingMemberships, newMembership]
          },
        },
      })
    },
  })

  const handleSubmit = (values: Values) =>
    createMembership({
      variables: {
        ...values,
        workspaceId,
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
