import React from "react"
import {
  Badge,
  Box,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
} from "@mui/material"
import { Link, useLocation } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"
import TooltipWrap from "components/utils/TooltipWrap"

export interface Page {
  title: string
  path: string
  icon: JSX.Element
  alt?: string
  className?: string
  alert?: boolean
  otherPaths?: string[]
}

const Icon: React.FC<{ selected: boolean; children: JSX.Element }> = ({
  selected,
  children,
}) => (
  <Box
    className="child-icon"
    sx={{
      backgroundColor: selected ? "#8338EC80" : null,
      color: selected ? "white" : "#747A82",
      borderRadius: "8px",
      height: 48,
      p: "12px",
    }}
  >
    {children}
  </Box>
)

type AppDrawerItemProps = {
  page: Page
  expanded: boolean
}

const AppDrawerItem: React.FC<AppDrawerItemProps> = ({ page, expanded }) => {
  const location = useLocation()
  const { routePrefix } = useWorkspace()

  const to = `${routePrefix}/${page.path}`

  const url = decodeURI(location.pathname)
  const otherPaths =
    page.otherPaths?.map(path => `${routePrefix}/${path}`) ?? []
  const selected = [to, ...otherPaths].some(path => url.startsWith(path))

  return (
    <ListItem disablePadding key={page.path} className={page.className}>
      <TooltipWrap show={!expanded} title={page.title} placement="right">
        <ListItemButton
          component={Link}
          to={to}
          sx={{
            ":hover .child-icon": {
              color: "white",
              backgroundColor: "#324459",
            },
            ":hover .child-text": {
              color: "white",
            },
          }}
        >
          <ListItemIcon sx={{ mr: "16px" }}>
            {page.alert ? (
              <Badge
                color="secondary"
                variant="dot"
                overlap="circular"
                data-testid="app-drawer-item-alert"
              >
                <Icon selected={selected}>{page.icon}</Icon>
              </Badge>
            ) : (
              <Icon selected={selected}>{page.icon}</Icon>
            )}
          </ListItemIcon>
          {expanded && (
            <ListItemText
              primary={page.title}
              primaryTypographyProps={{
                className: "child-text",
                sx: {
                  fontWeight: 600,
                  color: selected ? "white" : "#FFFFFF80",
                },
              }}
            />
          )}
        </ListItemButton>
      </TooltipWrap>
    </ListItem>
  )
}

export default AppDrawerItem
