import React from "react"
import {
  KeyboardArrowLeft,
  KeyboardArrowRight,
  Link as LinkIcon,
} from "@mui/icons-material"
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
import useLocalState from "helpers/useLocalState"
import useWorkspace from "helpers/useWorkspace"
import {
  Connections,
  GraiIcon,
  GraiLogoWhite,
  Graph,
  Reports,
  Tables,
} from "components/icons"
import ProfileMenu from "./ProfileMenu"

const pages = [
  {
    title: "Graph",
    path: "graph",
    icon: <Graph />,
    alt: "Graph",
  },
  {
    title: "Tables",
    path: "tables",
    icon: <Tables />,
    alt: "Tables",
  },
  {
    title: "Edges",
    path: "edges",
    icon: (
      <Box sx={{ p: "12px" }}>
        <LinkIcon
          sx={{
            color: "white",
            fontSize: 20,
            width: 24,
            height: 20,
          }}
        />
      </Box>
    ),
    alt: "Edges",
  },
  {
    title: "Connections",
    path: "connections",
    icon: <Connections />,
    alt: "Connections",
  },
  {
    title: "Reports",
    path: "reports",
    icon: <Reports />,
    alt: "Reports",
  },
]

const AppDrawer: React.FC = () => {
  const { routePrefix } = useWorkspace()
  const location = useLocation()

  const [expand, setExpand] = useLocalState("app-drawer", true)

  const drawerWidth = expand ? 224 : 81

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
            {expand ? <GraiLogoWhite /> : <GraiIcon />}
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
                  {page.icon}
                </Box>
              </ListItemIcon>
              {expand && (
                <ListItemText
                  primary={page.title}
                  primaryTypographyProps={{
                    sx: { fontWeight: 600, color: "#FFFFFF80" },
                  }}
                />
              )}
            </ListItemButton>
          </ListItem>
        ))}
        <ProfileMenu expand={expand} />
      </List>
      <List>
        {expand ? (
          <ListItem disablePadding>
            <ListItemButton onClick={() => setExpand(false)}>
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
                  <KeyboardArrowLeft sx={{ color: "#FFFFFF95" }} />
                </Box>
              </ListItemIcon>
              <ListItemText
                primary="Collapse"
                primaryTypographyProps={{
                  sx: { fontWeight: 600, color: "#FFFFFF80" },
                }}
              />
            </ListItemButton>
          </ListItem>
        ) : (
          <ListItem disablePadding>
            <ListItemButton onClick={() => setExpand(true)}>
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
                  <KeyboardArrowRight sx={{ color: "#FFFFFF95" }} />
                </Box>
              </ListItemIcon>
            </ListItemButton>
          </ListItem>
        )}
      </List>
    </Drawer>
  )
}

export default AppDrawer
