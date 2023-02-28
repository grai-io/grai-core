import React from "react"
import { MoreHoriz, Edit, Delete, DeleteOutline } from "@mui/icons-material"
import {
  IconButton,
  Menu,
  MenuItem,
  ListItemIcon,
  ListItemText,
} from "@mui/material"
import PopupState, { bindTrigger, bindMenu } from "material-ui-popup-state"

interface ApiKey {
  id: string
  name: string
}

type ApiKeyMenuProps = {
  apiKey: ApiKey
}

const ApiKeyMenu: React.FC<ApiKeyMenuProps> = ({ apiKey }) => {
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
            <MenuItem>
              <ListItemIcon>
                <Edit />
              </ListItemIcon>
              <ListItemText primary="Edit" />
            </MenuItem>
            <MenuItem>
              <ListItemIcon>
                <DeleteOutline />
              </ListItemIcon>
              <ListItemText primary="Revoke" />
            </MenuItem>
            <MenuItem>
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

export default ApiKeyMenu
