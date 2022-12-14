import {
  AccountCircle,
  Business,
  KeyboardArrowLeft,
  People,
  VpnKey,
} from "@mui/icons-material"
import {
  Box,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
} from "@mui/material"
import React, { useState } from "react"
import { Link, useParams } from "react-router-dom"

const drawerWidth = 300

const SettingsDrawer: React.FC = () => {
  const { workspaceId } = useParams()
  const [open, setOpen] = useState(true)

  const handleClose = () => setOpen(false)

  return (
    <Drawer
      variant="permanent"
      open={open}
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        "& .MuiDrawer-paper": {
          width: drawerWidth,
          boxSizing: "border-box",
        },
      }}
    >
      <Toolbar />
      <Box sx={{ display: "flex", flexDirection: "column", height: "100%" }}>
        <List sx={{ pt: 2 }}>
          <ListItem sx={{ py: 0 }}>
            <ListItemButton
              component={Link}
              to={`/workspaces/${workspaceId}/settings/profile`}
            >
              <ListItemIcon sx={{ minWidth: 0, mr: 2 }}>
                <AccountCircle />
              </ListItemIcon>
              <ListItemText primary="Profile" />
            </ListItemButton>
          </ListItem>
          <ListItem sx={{ py: 0 }}>
            <ListItemButton
              component={Link}
              to={`/workspaces/${workspaceId}/settings/api-keys`}
            >
              <ListItemIcon sx={{ minWidth: 0, mr: 2 }}>
                <VpnKey />
              </ListItemIcon>
              <ListItemText primary="API Keys" />
            </ListItemButton>
          </ListItem>
          <ListItem sx={{ py: 0 }}>
            <ListItemButton
              component={Link}
              to={`/workspaces/${workspaceId}/settings/workspace`}
            >
              <ListItemIcon sx={{ minWidth: 0, mr: 2 }}>
                <Business />
              </ListItemIcon>
              <ListItemText primary="Workspace Settings" />
            </ListItemButton>
          </ListItem>
          <ListItem sx={{ py: 0 }}>
            <ListItemButton
              component={Link}
              to={`/workspaces/${workspaceId}/settings/memberships`}
            >
              <ListItemIcon sx={{ minWidth: 0, mr: 2 }}>
                <People />
              </ListItemIcon>
              <ListItemText primary="Users" />
            </ListItemButton>
          </ListItem>
        </List>
        <Box sx={{ flexGrow: 1 }} />
        <List>
          <ListItem disablePadding>
            <ListItemButton onClick={handleClose}>
              <ListItemIcon sx={{ minWidth: 0, mr: 2 }}>
                <KeyboardArrowLeft />
              </ListItemIcon>
              <ListItemText primary="Collapse" />
            </ListItemButton>
          </ListItem>
        </List>
      </Box>
    </Drawer>
  )
}

export default SettingsDrawer
