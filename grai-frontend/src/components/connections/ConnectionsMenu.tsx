import { Delete, Edit, MoreHoriz } from "@mui/icons-material"
import {
  IconButton,
  ListItemIcon,
  ListItemText,
  Menu,
  MenuItem,
} from "@mui/material"
import PopupState, { bindMenu, bindTrigger } from "material-ui-popup-state"
import React from "react"
import { useNavigate, useParams } from "react-router-dom"
import ConnectionRefresh from "./ConnectionRefresh"

interface Run {
  id: string
  status: string
}

interface Connection {
  id: string
  last_run: Run | null
}

type ConnectionsMenuProps = {
  connection: Connection
}

const ConnectionsMenu: React.FC<ConnectionsMenuProps> = ({ connection }) => {
  const { workspaceId } = useParams()
  const navigate = useNavigate()

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
              onClick={() =>
                navigate(
                  `/workspaces/${workspaceId}/connections/${connection.id}`
                )
              }
            >
              <ListItemIcon>
                <Edit />
              </ListItemIcon>
              <ListItemText primary="Edit" />
            </MenuItem>
            <ConnectionRefresh connection={connection} menuItem disabled />
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
