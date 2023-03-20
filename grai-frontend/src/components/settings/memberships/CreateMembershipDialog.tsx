import React from "react"
import { gql, useMutation } from "@apollo/client"
import { Dialog, DialogContent } from "@mui/material"
import { useSnackbar } from "notistack"
import DialogTitle from "components/dialogs/DialogTitle"
import GraphError from "components/utils/GraphError"
import {
  CreateMemberships,
  CreateMembershipsVariables,
} from "./__generated__/CreateMemberships"
import { NewMembership } from "./__generated__/NewMembership"
import CreateMembershipForm, { Values } from "./forms/CreateMembershipForm"

export const CREATE_MEMBERSHIPS = gql`
  mutation CreateMemberships(
    $role: String!
    $emails: [String!]!
    $workspaceId: ID!
  ) {
    createMemberships(role: $role, emails: $emails, workspaceId: $workspaceId) {
      id
      role
      user {
        id
        username
        first_name
        last_name
      }
      is_active
      created_at
    }
  }
`

type CreateMembershipDialogProps = {
  workspaceId: string
  open: boolean
  onClose: () => void
}

const CreateMembershipDialog: React.FC<CreateMembershipDialogProps> = ({
  workspaceId,
  open,
  onClose,
}) => {
  const { enqueueSnackbar } = useSnackbar()

  const [createMemberships, { loading, error }] = useMutation<
    CreateMemberships,
    CreateMembershipsVariables
  >(CREATE_MEMBERSHIPS, {
    update(cache, { data }) {
      cache.modify({
        id: cache.identify({
          id: workspaceId,
          __typename: "Workspace",
        }),
        fields: {
          memberships(existingMemberships = []) {
            const newMemberships =
              data?.createMemberships.map(data =>
                cache.writeFragment<NewMembership>({
                  data,
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
              ) ?? []
            return [...existingMemberships, ...newMemberships]
          },
        },
      })
    },
  })

  const handleSubmit = (values: Values) =>
    createMemberships({
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
      <DialogTitle onClose={onClose}>Invite users</DialogTitle>
      <DialogContent>
        {error && <GraphError error={error} />}
        <CreateMembershipForm onSubmit={handleSubmit} loading={loading} />
      </DialogContent>
    </Dialog>
  )
}

export default CreateMembershipDialog
