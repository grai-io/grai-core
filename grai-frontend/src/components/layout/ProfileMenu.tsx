import React, { useState } from "react"
import { useApolloClient } from "@apollo/client"
import { Business, Logout, Settings } from "@mui/icons-material"
import {
  ListItem,
  ListItemButton,
  ListItemIcon,
  Box,
  ListItemText,
  Divider,
} from "@mui/material"
import posthog from "posthog"
import { Link } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"
import useAuth from "components/auth/useAuth"

type ProfileMenuProps = {
  expand?: boolean
}

const ProfileMenu: React.FC<ProfileMenuProps> = ({ expand }) => {
  const [open, setOpen] = useState(false)

  const { routePrefix } = useWorkspace()
  const { logoutUser } = useAuth()
  const client = useApolloClient()

  const handleLogout = () => {
    client.clearStore()
    logoutUser()
    posthog.reset()
    setOpen(false)
  }

  if (open) {
    return (
      <>
        <ListItem disablePadding>
          <ListItemButton onClick={() => setOpen(false)}>
            <ListItemIcon>
              <Box
                sx={{
                  borderRadius: "8px",
                  height: 48,
                  mr: "16px",
                }}
              >
                <img src="/icons/profile.svg" alt="Profile" />
              </Box>
            </ListItemIcon>
            {expand && (
              <ListItemText
                primary="Profile"
                primaryTypographyProps={{
                  sx: { fontWeight: 600, color: "#FFFFFF80" },
                }}
              />
            )}
          </ListItemButton>
        </ListItem>
        <Divider sx={{ backgroundColor: "#FFFFFF80", mx: 2 }} />
        <ListItem disablePadding>
          <ListItemButton component={Link} to={`${routePrefix}/settings`}>
            <ListItemIcon>
              <Box
                sx={{
                  borderRadius: "8px",
                  height: 48,
                  width: 48,
                  textAlign: "center",
                  pt: "10px",
                  mr: "16px",
                }}
              >
                <Settings sx={{ color: "#FFFFFF95" }} />
              </Box>
            </ListItemIcon>
            {expand && (
              <ListItemText
                primary="Settings"
                primaryTypographyProps={{
                  sx: { fontWeight: 600, color: "#FFFFFF80" },
                }}
              />
            )}
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton component={Link} to="/workspaces">
            <ListItemIcon>
              <Box
                sx={{
                  borderRadius: "8px",
                  height: 48,
                  width: 48,
                  textAlign: "center",
                  pt: "10px",
                  mr: "16px",
                }}
              >
                <Business sx={{ color: "#FFFFFF95" }} />
              </Box>
            </ListItemIcon>
            {expand && (
              <ListItemText
                primary="Workspaces"
                primaryTypographyProps={{
                  sx: { fontWeight: 600, color: "#FFFFFF80" },
                }}
              />
            )}
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton onClick={handleLogout}>
            <ListItemIcon>
              <Box
                sx={{
                  borderRadius: "8px",
                  height: 48,
                  width: 48,
                  textAlign: "center",
                  pt: "10px",
                  mr: "16px",
                }}
              >
                <Logout sx={{ color: "#FFFFFF95" }} />
              </Box>
            </ListItemIcon>
            {expand && (
              <ListItemText
                primary="Logout"
                primaryTypographyProps={{
                  sx: { fontWeight: 600, color: "#FFFFFF80" },
                }}
              />
            )}
          </ListItemButton>
        </ListItem>
      </>
    )
  }

  return (
    <ListItem disablePadding>
      <ListItemButton onClick={() => setOpen(true)}>
        <ListItemIcon>
          <Box
            sx={{
              borderRadius: "8px",
              height: 48,
              mr: "16px",
            }}
          >
            <img src="/icons/profile.svg" alt="Profile" />
          </Box>
        </ListItemIcon>
        {expand && (
          <ListItemText
            primary="Profile"
            primaryTypographyProps={{
              sx: { fontWeight: 600, color: "#FFFFFF80" },
            }}
          />
        )}
      </ListItemButton>
    </ListItem>
  )
}

export default ProfileMenu
