import {
  FilterAlt,
  KeyboardArrowLeft,
  KeyboardArrowRight,
  Refresh,
  Search,
} from "@mui/icons-material"
import { TabContext, TabList, TabPanel } from "@mui/lab"
import {
  Box,
  CircularProgress,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Tab,
  Tooltip,
} from "@mui/material"
import useLocalState from "helpers/useLocalState"
import React from "react"
import GraphSearch from "./GraphSearch"
import { Viewport } from "reactflow"

type GraphDrawerProps = {
  loading?: boolean
  onRefresh?: () => void
  onMove?: (viewport: Viewport) => void
}

const GraphDrawer: React.FC<GraphDrawerProps> = ({
  loading,
  onRefresh,
  onMove,
}) => {
  const [tab, setTab] = useLocalState<string | null>("graph-drawer", null)

  const expand = tab !== null

  const drawerWidth = expand ? 300 : 48

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
      anchor="right"
    >
      {expand ? (
        <Box sx={{ flexGrow: 1 }}>
          <TabContext value={tab}>
            <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
              <TabList
                centered
                value={tab}
                variant="fullWidth"
                onChange={(_, value) => value !== "refresh" && setTab(value)}
              >
                <Tab
                  onClick={onRefresh}
                  value="refresh"
                  label={
                    <Tooltip title="Refresh">
                      {loading ? <CircularProgress size="sm" /> : <Refresh />}
                    </Tooltip>
                  }
                  sx={{ minWidth: 0 }}
                />
                <Tab
                  value="search"
                  label={
                    <Tooltip title="Search">
                      <Search />
                    </Tooltip>
                  }
                  sx={{ minWidth: 0 }}
                />
                <Tab
                  value="filter"
                  label={
                    <Tooltip title="Filter">
                      <FilterAlt />
                    </Tooltip>
                  }
                  sx={{ minWidth: 0 }}
                />
              </TabList>
            </Box>
            <TabPanel value="search" sx={{ p: 0 }}>
              <GraphSearch onMove={onMove} />
            </TabPanel>
          </TabContext>
        </Box>
      ) : (
        <List sx={{ flexGrow: 1 }}>
          <ListItem disablePadding>
            <Tooltip title="Refresh">
              <ListItemButton
                onClick={onRefresh}
                sx={{
                  minHeight: 48,
                  justifyContent: "center",
                }}
              >
                <ListItemIcon
                  sx={{
                    minWidth: 0,
                    mr: "auto",
                    justifyContent: "center",
                  }}
                >
                  {loading ? <CircularProgress size="sm" /> : <Refresh />}
                </ListItemIcon>
              </ListItemButton>
            </Tooltip>
          </ListItem>
          <ListItem disablePadding>
            <Tooltip title="Search">
              <ListItemButton
                onClick={() => setTab("search")}
                sx={{
                  minHeight: 48,
                  justifyContent: "center",
                  px: 2.5,
                }}
              >
                <ListItemIcon
                  sx={{
                    minWidth: 0,
                    mr: "auto",
                    justifyContent: "center",
                  }}
                >
                  <Search />
                </ListItemIcon>
              </ListItemButton>
            </Tooltip>
          </ListItem>
          <ListItem disablePadding>
            <Tooltip title="Filter">
              <ListItemButton
                onClick={() => setTab("filter")}
                sx={{
                  minHeight: 48,
                  justifyContent: "center",
                  px: 2.5,
                }}
              >
                <ListItemIcon
                  sx={{
                    minWidth: 0,
                    mr: "auto",
                    justifyContent: "center",
                  }}
                >
                  <FilterAlt />
                </ListItemIcon>
              </ListItemButton>
            </Tooltip>
          </ListItem>
        </List>
      )}
      <List disablePadding>
        {expand ? (
          <ListItem disablePadding>
            <ListItemButton onClick={() => setTab(null)}>
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
                  <KeyboardArrowRight />
                </Box>
              </ListItemIcon>
              <ListItemText primary="Collapse" />
            </ListItemButton>
          </ListItem>
        ) : (
          <ListItem disablePadding>
            <ListItemButton
              onClick={() => setTab("search")}
              sx={{
                minHeight: 48,
                justifyContent: "center",
                px: 2.5,
              }}
            >
              <ListItemIcon
                sx={{
                  minWidth: 0,
                  mr: "auto",
                  justifyContent: "center",
                }}
              >
                <KeyboardArrowLeft />
              </ListItemIcon>
            </ListItemButton>
          </ListItem>
        )}
      </List>
    </Drawer>
  )
}

export default GraphDrawer
