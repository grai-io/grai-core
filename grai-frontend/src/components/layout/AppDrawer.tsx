import React from "react"
import {
  Box,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
} from "@mui/material"
import { Link, useLocation } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"
import ProfileMenuDrawer from "./ProfileMenuDrawer"

const pages = [
  {
    title: "Graph",
    path: "graph",
    icon: "/icons/graph.svg",
    alt: "Graph",
  },
  {
    title: "Tables",
    path: "tables",
    icon: "/icons/tables.svg",
    alt: "Tables",
  },
  {
    title: "Connections",
    path: "connections",
    icon: "/icons/connections.svg",
    alt: "Connections",
  },
  {
    title: "Reports",
    path: "reports",
    icon: "/icons/reports.svg",
    alt: "Reports",
  },
]

const drawerWidth = 224

const AppDrawer: React.FC = () => {
  const { routePrefix } = useWorkspace()
  const location = useLocation()

  return (
    <Drawer
      sx={{
        width: drawerWidth,
        display: "flex",
        flexShrink: 0,
        "& .MuiDrawer-paper": {
          width: drawerWidth,
          boxSizing: "border-box",
        },
      }}
      variant="permanent"
      anchor="left"
      PaperProps={{
        sx: {
          backgroundColor: "#1F2A37",
        },
      }}
    >
      <List>
        <ListItem disablePadding>
          <ListItemButton component={Link} to={`${routePrefix}`}>
            <img src="/images/grai-logo-single.svg" alt="Grai" />
          </ListItemButton>
        </ListItem>
      </List>
      <List sx={{ flexGrow: 1 }}>
        {pages.map(page => (
          <ListItem disablePadding key={page.path}>
            <ListItemButton component={Link} to={`${routePrefix}/${page.path}`}>
              <ListItemIcon>
                <Box
                  sx={{
                    backgroundColor: location.pathname.startsWith(
                      `${routePrefix}/${page.path}`
                    )
                      ? "#8338EC80"
                      : null,
                    borderRadius: "8px",
                    height: 48,
                    mr: "16px",
                  }}
                >
                  <img src={page.icon} alt={page.alt} />
                </Box>
              </ListItemIcon>
              <ListItemText
                primary={page.title}
                primaryTypographyProps={{
                  sx: { fontWeight: 600, color: "#FFFFFF80" },
                }}
              />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
      <ProfileMenuDrawer />
    </Drawer>
  )
}

export default AppDrawer
