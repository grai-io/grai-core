import React from "react"
import { useApolloClient } from "@apollo/client"
import { Menu, MenuItem } from "@mui/material"
import { bindMenu } from "material-ui-popup-state"
import { PopupState } from "material-ui-popup-state/hooks"
import posthog from "posthog"
import { Link } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"
import useAuth from "components/auth/useAuth"

type ProfileMenuProps = {
  popupState: PopupState
}

const ProfileMenu: React.FC<ProfileMenuProps> = ({ popupState }) => {
  const { routePrefix } = useWorkspace()
  const { logoutUser } = useAuth()
  const client = useApolloClient()

  const handleLogout = () => {
    client.clearStore()
    logoutUser()
    posthog.reset()
    popupState.close()
  }

  return (
    <Menu
      {...bindMenu(popupState)}
      anchorOrigin={{
        vertical: "center",
        horizontal: "right",
      }}
      transformOrigin={{
        vertical: "center",
        horizontal: "left",
      }}
      sx={{ ml: 2 }}
    >
      <MenuItem component={Link} to={`${routePrefix}/settings`}>
        Profile
      </MenuItem>
      <MenuItem component={Link} to="/workspaces">
        Change Workspace
      </MenuItem>
      <MenuItem onClick={handleLogout}>Logout</MenuItem>
    </Menu>
  )
}

export default ProfileMenu
