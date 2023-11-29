import React from "react"
import { Chat } from "@mui/icons-material"
import { Box, Drawer, List, ListItem, ListItemButton } from "@mui/material"
import { Link } from "react-router-dom"
import useChat from "helpers/useChat"
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

type AppDrawerProps = {
  profile?: User
  sampleData?: boolean
}

const AppDrawer: React.FC<AppDrawerProps> = ({ profile, sampleData }) => {
  const { routePrefix } = useWorkspace()
  const { unread } = useChat()
  const [expanded, setExpanded] = useLocalState("app-drawer", true)

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
      alert: unread,
    },
  ]

  const drawerWidth = expanded ? 224 : 81

  return (
    <>
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
              height: sampleData ? "calc(100vh - 64px)" : "100vh",
              position: "fixed",
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
              expanded={expanded}
              setExpanded={setExpanded}
              hover={hover}
            />
            <List>
              <ListItem disablePadding>
                <ListItemButton component={Link} to={`${routePrefix}`}>
                  {expanded ? <GraiLogoWhite /> : <GraiIcon />}
                </ListItemButton>
              </ListItem>
            </List>
            <List sx={{ flexGrow: 1 }}>
              {pages.map(page => (
                <AppDrawerItem
                  expanded={expanded}
                  key={page.path}
                  title={page.title}
                  path={page.path}
                  icon={page.icon}
                  className={page.className}
                  alert={page.alert}
                />
              ))}
            </List>
            <List>
              <AppDrawerItem
                title="Settings"
                path="settings/profile"
                icon={<Settings />}
                expanded={expanded}
              />

              <Profile expanded={expanded} profile={profile} />
            </List>
          </Drawer>
        )}
      </HoverState>
      <Box
        sx={{
          width: drawerWidth,
          flexShrink: 0,
        }}
      />
    </>
  )
}

export default AppDrawer
