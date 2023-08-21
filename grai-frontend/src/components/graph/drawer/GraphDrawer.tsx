import React from "react"
import {
  FilterAlt,
  FilterList,
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
import { Viewport } from "reactflow"
import useLocalState from "helpers/useLocalState"
import { Filter } from "components/filters/filters"
import GraphFilterInline from "./filters-inline/GraphFilterInline"
import GraphFilters from "./GraphFilters"
import GraphSearch from "./GraphSearch"

type GraphDrawerProps = {
  search: string
  onSearch: (search: string | null) => void
  loading?: boolean
  onRefresh?: () => void
  onMove?: (viewport: Viewport) => void
  filters: string[]
  setFilters: (filters: string[]) => void
  inlineFilters: Filter[]
  setInlineFilters: (filters: Filter[]) => void
}

const GraphDrawer: React.FC<GraphDrawerProps> = ({
  search,
  onSearch,
  loading,
  onRefresh,
  onMove,
  filters,
  setFilters,
  inlineFilters,
  setInlineFilters,
}) => {
  const [tab, setTab] = useLocalState<string | null>("graph-drawer", null)

  const expand = tab !== null

  const drawerWidth = expand ? 350 : 48

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
                  className="graph-search"
                />
                <Tab
                  value="filter"
                  label={
                    <Tooltip title="Filter">
                      <FilterAlt />
                    </Tooltip>
                  }
                  sx={{ minWidth: 0 }}
                  className="graph-filter"
                />
                <Tab
                  value="filter-list"
                  label={
                    <Tooltip title="Filter List">
                      <FilterList />
                    </Tooltip>
                  }
                  sx={{ minWidth: 0 }}
                  className="graph-filter-list"
                />
              </TabList>
            </Box>
            <TabPanel value="search" sx={{ p: 0 }}>
              <GraphSearch
                onMove={onMove}
                search={search}
                onSearch={onSearch}
              />
            </TabPanel>
            <TabPanel value="filter" sx={{ p: 0 }}>
              <GraphFilterInline
                inlineFilters={inlineFilters}
                setInlineFilters={setInlineFilters}
              />
            </TabPanel>
            <TabPanel value="filter-list" sx={{ p: 0 }}>
              <GraphFilters filters={filters} setFilters={setFilters} />
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
          <ListItem disablePadding className="graph-search">
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
          <ListItem disablePadding>
            <Tooltip title="Filter List">
              <ListItemButton
                onClick={() => setTab("filter-list")}
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
                  <FilterList />
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
