import React from "react"
import {
  AccountCircle,
  Business,
  CloudQueue,
  Lock,
  Notifications,
  People,
  VpnKey,
} from "@mui/icons-material"
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  ListSubheader,
  Typography,
} from "@mui/material"
import { Link } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"

const Subheader = ({ children }: { children: React.ReactNode }) => (
  <ListSubheader
    sx={{
      color: "#79797D",
      fontSize: "14px",
      fontWeight: 500,
      textTransform: "uppercase",
      backgroundColor: "#F8F8F8",
      fontFamily: "Inter",
      pl: "24px",
    }}
  >
    {children}
  </ListSubheader>
)

const drawerWidth = 300

const SettingsDrawer: React.FC = () => {
  const { routePrefix } = useWorkspace()

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        "& .MuiDrawer-paper": {
          marginLeft: "76px",
          width: drawerWidth,
          boxSizing: "border-box",
          backgroundColor: "#F8F8F8",
        },
      }}
    >
      <Typography
        sx={{
          pl: "24px",
          pt: "32px",
          color: "rgba(0, 0, 0, 0.80)",
          fontSize: "18px",
          fontWeight: 700,
        }}
      >
        Settings
      </Typography>
      <List sx={{ pt: 2 }}>
        <Subheader>Profile</Subheader>
        <ListItem sx={{ py: 0 }}>
          <ListItemButton
            component={Link}
            to={`${routePrefix}/settings/profile`}
          >
            <ListItemIcon sx={{ minWidth: 0, mr: 2 }}>
              <AccountCircle />
            </ListItemIcon>
            <ListItemText primary="Personal info" />
          </ListItemButton>
        </ListItem>
        <ListItem sx={{ py: 0 }}>
          <ListItemButton component={Link} to={`${routePrefix}/settings/2fa`}>
            <ListItemIcon sx={{ minWidth: 0, mr: 2 }}>
              <Lock />
            </ListItemIcon>
            <ListItemText primary="2 Factor" />
          </ListItemButton>
        </ListItem>
        <ListItem sx={{ py: 0 }}>
          <ListItemButton
            component={Link}
            to={`${routePrefix}/settings/api-keys`}
          >
            <ListItemIcon sx={{ minWidth: 0, mr: 2 }}>
              <VpnKey />
            </ListItemIcon>
            <ListItemText primary="API Keys" />
          </ListItemButton>
        </ListItem>
      </List>
      <List sx={{ pt: "36px" }}>
        <Subheader>Workspace Settings</Subheader>
        <ListItem sx={{ py: 0 }}>
          <ListItemButton
            component={Link}
            to={`${routePrefix}/settings/workspace`}
          >
            <ListItemIcon sx={{ minWidth: 0, mr: 2 }}>
              <Business />
            </ListItemIcon>
            <ListItemText primary="Settings" />
          </ListItemButton>
        </ListItem>
        <ListItem sx={{ py: 0 }}>
          <ListItemButton
            component={Link}
            to={`${routePrefix}/settings/memberships`}
          >
            <ListItemIcon sx={{ minWidth: 0, mr: 2 }}>
              <People />
            </ListItemIcon>
            <ListItemText primary="Users" />
          </ListItemButton>
        </ListItem>
        <ListItem sx={{ py: 0 }}>
          <ListItemButton
            component={Link}
            to={`${routePrefix}/settings/alerts`}
          >
            <ListItemIcon sx={{ minWidth: 0, mr: 2 }}>
              <Notifications />
            </ListItemIcon>
            <ListItemText primary="Alerts" />
          </ListItemButton>
        </ListItem>
        <ListItem sx={{ py: 0 }}>
          <ListItemButton
            component={Link}
            to={`${routePrefix}/settings/installations`}
          >
            <ListItemIcon sx={{ minWidth: 0, mr: 2 }}>
              <CloudQueue />
            </ListItemIcon>
            <ListItemText primary="Installations" />
          </ListItemButton>
        </ListItem>
      </List>
    </Drawer>
  )
}

export default SettingsDrawer
