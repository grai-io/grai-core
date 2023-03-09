import React from "react"
import { MoreHoriz, Edit } from "@mui/icons-material"
import {
  IconButton,
  Menu,
  MenuItem,
  ListItemIcon,
  ListItemText,
} from "@mui/material"
import PopupState, { bindMenu, bindTrigger } from "material-ui-popup-state"
import MembershipDelete, { Membership } from "./MembershipDelete"

type MembershipMenuProps = {
  membership: Membership
  workspaceId?: string
}

const MembershipMenu: React.FC<MembershipMenuProps> = ({
  membership,
  workspaceId,
}) => (
  <PopupState variant="popover">
    {popupState => (
      <>
        <IconButton size="small" {...bindTrigger(popupState)}>
          <MoreHoriz />
        </IconButton>

        <Menu
          {...bindMenu(popupState)}
          PaperProps={{
            sx: {
              width: 200,
            },
          }}
        >
          <MenuItem disabled>
            <ListItemIcon>
              <Edit />
            </ListItemIcon>
            <ListItemText primary="Edit" />
          </MenuItem>
          <MembershipDelete
            membership={membership}
            onClose={popupState.close}
            workspaceId={workspaceId}
          />
        </Menu>
      </>
    )}
  </PopupState>
)

export default MembershipMenu
