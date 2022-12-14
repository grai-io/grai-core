import { useApolloClient } from "@apollo/client"
import { AccountCircle, Settings, Business, Logout } from "@mui/icons-material"
import {
  IconButton,
  Menu,
  Box,
  Divider,
  MenuItem,
  ListItemIcon,
  ListItemText,
} from "@mui/material"
import PopupState, {
  bindMenu,
  bindTrigger,
  InjectedProps,
} from "material-ui-popup-state"
import React, { useContext } from "react"
import { Link, useParams } from "react-router-dom"
import AuthContext from "../auth/AuthContext"

const ProfileMenu: React.FC = () => {
  const { workspaceId } = useParams()
  const { logoutUser } = useContext(AuthContext)
  const client = useApolloClient()

  const handleLogout = (popupState: InjectedProps) => {
    client.clearStore()
    logoutUser()
    popupState.close()
  }

  return (
    <PopupState variant="popover" popupId="demo-popup-menu">
      {popupState => (
        <React.Fragment>
          <IconButton
            {...bindTrigger(popupState)}
            data-testid="profile-menu-open"
          >
            <AccountCircle color="secondary" />
          </IconButton>
          <Menu {...bindMenu(popupState)}>
            <Box sx={{ mx: 2 }}>
              {/* <Typography>{data?.me?.name}</Typography>
              <Typography variant="body2">{data?.me?.email}</Typography> */}
            </Box>
            <Divider sx={{ my: 1 }} />
            <MenuItem
              onClick={popupState.close}
              component={Link}
              to={`/workspaces/${workspaceId}/settings`}
            >
              <ListItemIcon>
                <Settings fontSize="small" />
              </ListItemIcon>
              <ListItemText>Settings</ListItemText>
            </MenuItem>

            <MenuItem
              onClick={popupState.close}
              component={Link}
              to="/workspaces"
            >
              <ListItemIcon>
                <Business fontSize="small" />
              </ListItemIcon>
              <ListItemText>Change Workspace</ListItemText>
            </MenuItem>

            <MenuItem onClick={() => handleLogout(popupState)}>
              <ListItemIcon>
                <Logout fontSize="small" />
              </ListItemIcon>
              <ListItemText>Logout</ListItemText>
            </MenuItem>
          </Menu>
        </React.Fragment>
      )}
    </PopupState>
  )
}

export default ProfileMenu
