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
import { useNavigate } from "react-router-dom"
import ConnectionRefresh from "./ConnectionRefresh"

interface Connection {
  id: string
}

type ConnectionsMenuProps = {
  connection: Connection
}

const ConnectionsMenu: React.FC<ConnectionsMenuProps> = ({ connection }) => {
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
            <MenuItem onClick={() => navigate(`/connections/${connection.id}`)}>
              <ListItemIcon>
                <Edit />
              </ListItemIcon>
              <ListItemText primary="Edit" />
            </MenuItem>
            <ConnectionRefresh connection={connection} menuItem />
            <MenuItem>
              <ListItemIcon>
                <Delete />
              </ListItemIcon>
              <ListItemText primary="Delete" />
            </MenuItem>
            {/* <RefreshButton
              source={table.source}
              menuItem
              onClose={popupState.close} />
            <ExportButton
              tableId={table.id}
              menuItem
              onClose={popupState.close} />
            <TableDeleteButton table={table} onClose={popupState.close} /> */}
          </Menu>
        </>
      )}
    </PopupState>
  )
}

export default ConnectionsMenu
