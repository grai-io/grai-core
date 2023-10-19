import React from "react"
import {
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  ListSubheader,
  SxProps,
} from "@mui/material"
import { Link, useLocation } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"

const Subheader = ({ children }: { children: React.ReactNode }) => (
  <ListSubheader
    sx={{
      color: "#79797D",
      fontSize: "14px",
      fontWeight: 500,
      textTransform: "uppercase",
      backgroundColor: "#F8F8F8",
      fontFamily: "Inter",
      pl: "24px",
    }}
  >
    {children}
  </ListSubheader>
)

export interface Page {
  name: string
  icon: React.ReactNode
  path: string
}

type SettingsDrawerSectionProps = {
  title: string
  pages: Page[]
  sx?: SxProps
}

const SettingsDrawerSection: React.FC<SettingsDrawerSectionProps> = ({
  title,
  pages,
  sx,
}) => {
  const { routePrefix } = useWorkspace()
  const location = useLocation()

  return (
    <List sx={sx}>
      <Subheader>{title}</Subheader>
      {pages.map(({ name, icon, path }) => (
        <ListItem sx={{ py: 0 }} key={name} disableGutters>
          <ListItemButton
            component={Link}
            to={routePrefix + path}
            selected={location.pathname === routePrefix + path}
            sx={{ pl: "24px" }}
          >
            <ListItemIcon sx={{ minWidth: 0, mr: 2 }}>{icon}</ListItemIcon>
            <ListItemText primary={name} />
          </ListItemButton>
        </ListItem>
      ))}
    </List>
  )
}

export default SettingsDrawerSection
