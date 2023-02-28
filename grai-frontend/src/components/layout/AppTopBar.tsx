import React from "react"
import { AppBar, Toolbar, Button, Box } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import { Link } from "react-router-dom"
import ProfileMenu from "./ProfileMenu"

const AppTopBar: React.FC = () => {
  const { routePrefix } = useWorkspace()

  return (
    <AppBar position="static">
      <Toolbar>
        <Box component={Link} to={routePrefix} sx={{ mt: 1 }}>
          <img src="/images/grai-logo-single.svg" alt="Grai" />
        </Box>
        <Button
          component={Link}
          to={`${routePrefix}/graph`}
          sx={{ my: 2, color: "inherit" }}
        >
          Graph
        </Button>
        <Button
          component={Link}
          to={`${routePrefix}/tables`}
          sx={{ my: 2, color: "inherit" }}
        >
          Tables
        </Button>
        <Button
          component={Link}
          to={`${routePrefix}/connections`}
          sx={{ my: 2, color: "inherit" }}
        >
          Connections
        </Button>
        <Button
          component={Link}
          to={`${routePrefix}/reports`}
          sx={{ my: 2, color: "inherit" }}
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
