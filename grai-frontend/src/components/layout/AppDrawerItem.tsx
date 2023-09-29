import {
  Box,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
} from "@mui/material"
import TooltipWrap from "components/utils/TooltipWrap"
import useWorkspace from "helpers/useWorkspace"
import React from "react"
import { Link } from "react-router-dom"

export type Page = {
  title: string
  path: string
  icon: JSX.Element
  alt: string
  className?: string
}

type AppDrawerItemProps = {
  page: Page
  expand: boolean
}

const AppDrawerItem: React.FC<AppDrawerItemProps> = ({ page, expand }) => {
  const { routePrefix } = useWorkspace()

  const selected = decodeURI(location.pathname).startsWith(
    `${routePrefix}/${page.path}`,
  )

  return (
    <ListItem disablePadding key={page.path} className={page.className}>
      <TooltipWrap show={!expand} title={page.title} placement="right">
        <ListItemButton component={Link} to={`${routePrefix}/${page.path}`}>
          <ListItemIcon>
            <Box
              sx={{
                backgroundColor: selected ? "#8338EC80" : null,
                color: selected ? "white" : "#747A82",
                borderRadius: "8px",
                height: 48,
                mr: "16px",
                p: "12px",
              }}
            >
              {page.icon}
            </Box>
          </ListItemIcon>
          {expand && (
            <ListItemText
              primary={page.title}
              primaryTypographyProps={{
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
