import React from "react"
import { Edit } from "@mui/icons-material"
import { MenuItem, ListItemIcon, ListItemText } from "@mui/material"
import PopupState, { bindMenu, bindTrigger } from "material-ui-popup-state"
import EditMembershipDialog from "./EditMembershipDialog"

interface User {
  first_name: string | null
  last_name: string | null
  username: string | null
}

export interface Membership {
  id: string
  role: string
  is_active: boolean
  user: User
}

type MembershipEditProps = {
  membership: Membership
  onClose: () => void
}

const MembershipEdit: React.FC<MembershipEditProps> = ({
  membership,
  onClose,
}) => (
  <PopupState variant="popover">
    {popupState => (
      <>
        <MenuItem {...bindTrigger(popupState)}>
          <ListItemIcon>
            <Edit />
          </ListItemIcon>
          <ListItemText primary="Edit" />
        </MenuItem>

        <EditMembershipDialog
          membership={membership}
          {...bindMenu(popupState)}
          onClose={onClose}
        />
      </>
    )}
  </PopupState>
)

export default MembershipEdit
