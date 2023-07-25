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
import SourceDelete from "./SourceDelete"

interface Source {
  id: string
  name: string
}

type SourcesMenuProps = {
  source: Source
  workspaceId: string
}

const SourcesMenu: React.FC<SourcesMenuProps> = ({ source, workspaceId }) => (
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
          <MenuItem component={Link} to={source.id}>
            <ListItemIcon>
              <Edit />
            </ListItemIcon>
            <ListItemText primary="Edit" />
          </MenuItem>
          <SourceDelete
            source={source}
            onClose={popupState.close}
            workspaceId={workspaceId}
          />
        </Menu>
      </>
    )}
  </PopupState>
)

export default SourcesMenu
