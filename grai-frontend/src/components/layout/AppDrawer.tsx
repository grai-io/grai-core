import React from "react"
import {
  Box,
  Drawer,
  Fade,
  List,
  ListItem,
  ListItemButton,
} from "@mui/material"
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
import AppDrawerItem from "./AppDrawerItem"
import Profile from "./profile/Profile"

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
    <HoverState>
      {(hover, bindHover, setHover) => (
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
          <Fade in={hover} timeout={{ exit: 500 }}>
            {expand ? (
              <Box
                sx={{
                  p: "2px",
                  borderRadius: 40,
                  backgroundColor: "#324459",
                  left: 212,
                  top: 24,
                  position: "absolute",
                  width: "24px",
                  height: "24px",
                  zIndex: 20,
                  cursor: "pointer",
                }}
                onClick={() => setExpand(false)}
              >
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 20 20"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <g id="Icon set">
                    <path
                      id="Vector"
                      d="M8.12504 9.99992L11.5417 13.4166C11.6945 13.5694 11.7709 13.7464 11.7709 13.9478C11.7709 14.1492 11.6945 14.3263 11.5417 14.4791C11.3889 14.6319 11.2118 14.7083 11.0105 14.7083C10.8091 14.7083 10.6296 14.6295 10.4722 14.472L6.52087 10.5208C6.45143 10.4458 6.39935 10.3645 6.36462 10.277C6.3299 10.1895 6.31254 10.0958 6.31254 9.99575C6.31254 9.89575 6.3299 9.802 6.36462 9.7145C6.39935 9.627 6.45143 9.54853 6.52087 9.47909L10.4722 5.52779C10.6296 5.37032 10.8056 5.29506 11 5.302C11.1945 5.30895 11.3681 5.38881 11.5209 5.54158C11.6737 5.69436 11.75 5.87145 11.75 6.07283C11.75 6.27422 11.6737 6.45131 11.5209 6.60408L8.12504 9.99992Z"
                      fill="#C0C3C7"
                    />
                  </g>
                </svg>
              </Box>
            ) : (
              <Box
                sx={{
                  p: "2px",
                  borderRadius: 40,
                  backgroundColor: "#324459",
                  left: 68,
                  top: 24,
                  position: "absolute",
                  width: "24px",
                  height: "24px",
                  zIndex: 20,
                  cursor: "pointer",
                }}
                onClick={() => setExpand(true)}
              >
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 20 20"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M11.8748 10.0001L8.45817 6.58341C8.30539 6.43064 8.229 6.25355 8.229 6.05216C8.229 5.85078 8.30539 5.67369 8.45817 5.52091C8.61095 5.36814 8.78803 5.29175 8.98942 5.29175C9.19081 5.29175 9.37024 5.37048 9.52771 5.52796L13.479 9.47925C13.5484 9.55425 13.6005 9.6355 13.6353 9.723C13.67 9.8105 13.6873 9.90425 13.6873 10.0042C13.6873 10.1042 13.67 10.198 13.6353 10.2855C13.6005 10.373 13.5484 10.4515 13.479 10.5209L9.52771 14.4722C9.37024 14.6297 9.19428 14.7049 8.99984 14.698C8.80539 14.6911 8.63178 14.6112 8.479 14.4584C8.32623 14.3056 8.24984 14.1286 8.24984 13.9272C8.24984 13.7258 8.32623 13.5487 8.479 13.3959L11.8748 10.0001Z"
                    fill="#C0C3C7"
                  />
                </svg>
              </Box>
            )}
          </Fade>
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

            <Profile expand={expand} />
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
