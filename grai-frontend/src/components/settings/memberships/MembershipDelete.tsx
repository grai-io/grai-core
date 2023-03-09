import React from "react"
import { gql, useMutation } from "@apollo/client"
import { Delete } from "@mui/icons-material"
import { MenuItem, ListItemIcon, ListItemText } from "@mui/material"
import { useConfirm } from "material-ui-confirm"
import { useSnackbar } from "notistack"
import {
  DeleteMembership,
  DeleteMembershipVariables,
} from "./__generated__/DeleteMembership"

export const DELETE_MEMBERSHIP = gql`
  mutation DeleteMembership($id: ID!) {
    deleteMembership(id: $id) {
      id
    }
  }
`

interface User {
  first_name: string | null
  last_name: string | null
  username: string | null
}

export interface Membership {
  id: string
  user: User
}

type MembershipDeleteProps = {
  membership: Membership
  workspaceId?: string
  onClose: () => void
}

const MembershipDelete: React.FC<MembershipDeleteProps> = ({
  membership,
  workspaceId,
  onClose,
}) => {
  const confirm = useConfirm()
  const { enqueueSnackbar } = useSnackbar()

  const [deleteMembership] = useMutation<
    DeleteMembership,
    DeleteMembershipVariables
  >(DELETE_MEMBERSHIP, {
    variables: { id: membership.id },
    update(cache, { data }) {
      cache.modify({
        id: cache.identify({
          id: workspaceId,
          __typename: "Workspace",
        }),
        fields: {
          memberships: (existingMemberships, { readField }) =>
            existingMemberships.filter(
              (keyRef: any) =>
                data?.deleteMembership.id !== readField("id", keyRef)
            ),
        },
      })
    },
  })

  const handleDelete = () =>
    confirm({
      title: "Delete Membership",
      description: `Are you sure you wish to delete the ${
        membership.user.first_name
          ? `${membership.user.first_name} ${membership.user.last_name}`
          : membership.user.username
      } membership?`,
      confirmationText: "Delete",
    })
      .then(() => deleteMembership())
      .then(() => enqueueSnackbar("Membership deleted", { variant: "success" }))
      .finally(() => onClose())

  return (
    <MenuItem onClick={handleDelete}>
      <ListItemIcon>
        <Delete />
      </ListItemIcon>
      <ListItemText primary="Delete" />
    </MenuItem>
  )
}

export default MembershipDelete
