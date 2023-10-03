import React from "react"
import {
  Box,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
} from "@mui/material"
import { Link, useLocation } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"
import TooltipWrap from "components/utils/TooltipWrap"

type AppDrawerItemProps = {
  title: string
  path: string
  icon: JSX.Element
  className?: string
  expand: boolean
}

const AppDrawerItem: React.FC<AppDrawerItemProps> = ({
  title,
  path,
  icon,
  className,
  expand,
}) => {
  const location = useLocation()
  const { routePrefix } = useWorkspace()

  const to = `${routePrefix}/${path}`

  const selected = decodeURI(location.pathname).startsWith(to)

  return (
    <ListItem disablePadding key={path} className={className}>
      <TooltipWrap show={!expand} title={title} placement="right">
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
          <ListItemIcon>
            <Box
              className="child-icon"
              sx={{
                backgroundColor: selected ? "#8338EC80" : null,
                color: selected ? "white" : "#747A82",
                borderRadius: "8px",
                height: 48,
                mr: "16px",
                p: "12px",
              }}
            >
              {icon}
            </Box>
          </ListItemIcon>
          {expand && (
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
