import React from "react"
import { Edit, MoreHoriz } from "@mui/icons-material"
import {
  IconButton,
  ListItemIcon,
  ListItemText,
  Menu,
  MenuItem,
} from "@mui/material"
import PopupState, { bindMenu, bindTrigger } from "material-ui-popup-state"
import { Link } from "react-router-dom"
import AlertDelete from "./AlertDelete"

interface Alert {
  id: string
  name: string
}

type AlertMenuProps = {
  alert: Alert
  workspaceId?: string
}

const AlertMenu: React.FC<AlertMenuProps> = ({ alert, workspaceId }) => (
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
          <MenuItem component={Link} to={alert.id}>
            <ListItemIcon>
              <Edit />
            </ListItemIcon>
            <ListItemText primary="Edit" />
          </MenuItem>
          <AlertDelete
            alert={alert}
            onClose={popupState.close}
            workspaceId={workspaceId}
          />
        </Menu>
      </>
    )}
  </PopupState>
)

export default AlertMenu
