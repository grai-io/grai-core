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
  Nodes,
} from "components/icons"
import ProfileMenu from "./ProfileMenu"
import Edge from "components/icons/Edge"
import AppDrawerItem from "./AppDrawerItem"

const pages = [
  {
    title: "Graph",
    path: "graph",
    icon: <Graph />,
    alt: "Graph",
    className: "graph-page",
  },
  {
    title: "Nodes",
    path: "nodes",
    icon: <Nodes />,
    alt: "Nodes",
  },
  {
    title: "Edges",
    path: "edges",
    icon: <Edge />,
    alt: "Edges",
  },
  {
    title: "Sources",
    path: "sources",
    icon: <Connections />,
    alt: "Sources",
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
          <AppDrawerItem page={page} expand={expand} key={page.path} />
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
