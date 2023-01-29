import { Delete, Edit, MoreHoriz } from "@mui/icons-material"
import {
  IconButton,
  ListItemIcon,
  ListItemText,
  Menu,
  MenuItem,
} from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import PopupState, { bindMenu, bindTrigger } from "material-ui-popup-state"
import React from "react"
import ConnectionRefresh, { Connection } from "./ConnectionRefresh"

type ConnectionsMenuProps = {
  connection: Connection
  workspaceId: string
}

const ConnectionsMenu: React.FC<ConnectionsMenuProps> = ({
  connection,
  workspaceId,
}) => {
  const { workspaceNavigate } = useWorkspace()

  return (
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
            <MenuItem
              onClick={() => workspaceNavigate(`connections/${connection.id}`)}
            >
              <ListItemIcon>
                <Edit />
              </ListItemIcon>
              <ListItemText primary="Edit" />
            </MenuItem>
            <ConnectionRefresh
              connection={connection}
              workspaceId={workspaceId}
              menuItem
              disabled
            />
            <MenuItem disabled>
              <ListItemIcon>
                <Delete />
              </ListItemIcon>
              <ListItemText primary="Delete" />
            </MenuItem>
          </Menu>
        </>
      )}
    </PopupState>
  )
}

export default ConnectionsMenu
