import React from "react"
import { AppBar, Toolbar, Typography, Button, Link } from "@mui/material"
import { Link as RouterLink } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"

const GettingStarted: React.FC = () => {
  const { routePrefix } = useWorkspace()

  return (
    <AppBar position="static" color="secondary">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Getting Started
        </Typography>
        <Button
          variant="contained"
          color="info"
          component={RouterLink}
          to={`${routePrefix}/connections/create`}
        >
          Create Source
        </Button>
        <Button
          variant="contained"
          color="info"
          sx={{ ml: 1 }}
          component={Link}
          href="https://docs.grai.io"
          target="_blank"
        >
          Docs
        </Button>
      </Toolbar>
    </AppBar>
  )
}

export default GettingStarted
