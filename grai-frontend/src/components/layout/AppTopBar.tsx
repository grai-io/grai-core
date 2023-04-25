import React from "react"
import { AppBar, Toolbar, Button, Box } from "@mui/material"
import { Link } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"
import ProfileMenu from "./ProfileMenu"

const AppTopBar: React.FC = () => {
  const { routePrefix } = useWorkspace()

  return (
    <AppBar position="static">
      <Toolbar>
        <Box component={Link} to={routePrefix} sx={{ mt: 1 }}>
          <img src="/icons/grai/grai-logo-single.svg" alt="Grai" />
        </Box>
        <Button
          component={Link}
          to={`${routePrefix}/graph`}
          sx={{ my: 2, color: theme => theme.palette.secondary.main }}
        >
          Graph
        </Button>
        <Button
          component={Link}
          to={`${routePrefix}/tables`}
          sx={{ my: 2, color: theme => theme.palette.secondary.main }}
        >
          Tables
        </Button>
        <Button
          component={Link}
          to={`${routePrefix}/connections`}
          sx={{ my: 2, color: theme => theme.palette.secondary.main }}
        >
          Connections
        </Button>
        <Button
          component={Link}
          to={`${routePrefix}/reports`}
          sx={{ my: 2, color: theme => theme.palette.secondary.main }}
        >
          Reports
        </Button>
        <Box sx={{ flexGrow: 1 }} />
        <ProfileMenu />
      </Toolbar>
    </AppBar>
  )
}

export default AppTopBar
