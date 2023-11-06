import React from "react"
import { Drawer, List, ListItem, ListItemButton } from "@mui/material"
import { Link } from "react-router-dom"
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
import Edge from "components/icons/Edge"
import Settings from "components/icons/Settings"
import HoverState from "components/utils/HoverState"
import AppDrawerCollapse from "./AppDrawerCollapse"
import AppDrawerItem from "./AppDrawerItem"
import Profile, { User } from "./profile/Profile"
import { Chat } from "@mui/icons-material"

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
  {
    title: "Chat",
    path: "chat",
    icon: <Chat />,
    alt: "Chat",
  },
]

type AppDrawerProps = {
  profile?: User
}

const AppDrawer: React.FC<AppDrawerProps> = ({ profile }) => {
  const { routePrefix } = useWorkspace()
  const [expand, setExpand] = useLocalState("app-drawer", true)

  const drawerWidth = expand ? 224 : 81

  return (
    <HoverState>
      {(hover, bindHover) => (
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
              position: "static",
            },
          }}
          {...bindHover}
        >
          <AppDrawerCollapse
            expand={expand}
            setExpand={setExpand}
            hover={hover}
          />
          <List>
            <ListItem disablePadding>
              <ListItemButton component={Link} to={`${routePrefix}`}>
                {expand ? <GraiLogoWhite /> : <GraiIcon />}
              </ListItemButton>
            </ListItem>
          </List>
          <List sx={{ flexGrow: 1 }}>
            {pages.map(page => (
              <AppDrawerItem
                expand={expand}
                key={page.path}
                title={page.title}
                path={page.path}
                icon={page.icon}
                className={page.className}
              />
            ))}
          </List>
          <List>
            <AppDrawerItem
              title="Settings"
              path="settings/profile"
              icon={<Settings />}
              expand={expand}
            />

            <Profile expand={expand} profile={profile} />
            {/* {expand ? (
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
          )} */}
          </List>
        </Drawer>
      )}
    </HoverState>
  )
}

export default AppDrawer
