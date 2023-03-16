import React from "react"
import { MoreHoriz } from "@mui/icons-material"
import { IconButton, Menu } from "@mui/material"
import PopupState, { bindMenu, bindTrigger } from "material-ui-popup-state"
import MembershipDelete from "./MembershipDelete"
import MembershipEdit, { Membership } from "./MembershipEdit"

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
          <MembershipEdit membership={membership} onClose={popupState.close} />
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
