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
  edit?: boolean
}

const FiltersMenu: React.FC<FiltersMenuProps> = ({
  filter,
  workspaceId,
  edit,
}) => (
  <PopupState variant="popover">
    {popupState => {
      // Create a handler function that matches the expected type for onClose
      const handleDeleteClose = (deleted: boolean) => {
        // You can handle the 'deleted' boolean as needed
        popupState.close(); // Call the original close method without arguments
      };

      return (
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
            {edit && (
              <MenuItem component={Link} to={filter.id}>
                <ListItemIcon>
                  <Edit />
                </ListItemIcon>
                <ListItemText primary="Edit" />
              </MenuItem>
            )}
            <FilterDelete
              filter={filter}
              onClose={handleDeleteClose} // Use the new handler function
              workspaceId={workspaceId}
            />
          </Menu>
        </>
      )
    }}
  </PopupState>
)

export default FiltersMenu
