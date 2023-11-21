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
  title: string
  path: string
  icon: JSX.Element
  className?: string
  expanded: boolean
  alert?: boolean
}

const AppDrawerItem: React.FC<AppDrawerItemProps> = ({
  title,
  path,
  icon,
  className,
  expanded,
  alert,
}) => {
  const location = useLocation()
  const { routePrefix } = useWorkspace()

  const to = `${routePrefix}/${path}`

  const selected = decodeURI(location.pathname).startsWith(to)

  return (
    <ListItem disablePadding key={path} className={className}>
      <TooltipWrap show={!expanded} title={title} placement="right">
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
            {alert ? (
              <Badge
                color="secondary"
                variant="dot"
                overlap="circular"
                data-testid="app-drawer-item-alert"
              >
                <Icon selected={selected}>{icon}</Icon>
              </Badge>
            ) : (
              <Icon selected={selected}>{icon}</Icon>
            )}
          </ListItemIcon>
          {expanded && (
            <ListItemText
              primary={title}
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
