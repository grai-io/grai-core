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
import FilterDelete, { Filter } from "./FilterDelete"

type FiltersMenuProps = {
  filter: Filter
  workspaceId: string
}

const FiltersMenu: React.FC<FiltersMenuProps> = ({ filter, workspaceId }) => (
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
          <MenuItem component={Link} to={filter.id}>
            <ListItemIcon>
              <Edit />
            </ListItemIcon>
            <ListItemText primary="Edit" />
          </MenuItem>
          <FilterDelete
            filter={filter}
            onClose={popupState.close}
            workspaceId={workspaceId}
          />
        </Menu>
      </>
    )}
  </PopupState>
)

export default FiltersMenu
