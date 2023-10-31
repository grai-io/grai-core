import React from "react"
import { AppBar, Toolbar, Typography, Button, Link } from "@mui/material"
import { Link as RouterLink } from "react-router-dom"

interface Organisation {
  id: string
}

interface Workspace {
  organisation: Organisation
}

type SampleDataProps = {
  workspace: Workspace
}

const SampleData: React.FC<SampleDataProps> = ({ workspace }) => (
  <AppBar position="static" color="secondary">
    <Toolbar>
      <Typography variant="body1" component="div" sx={{ flexGrow: 1 }}>
        Welcome to your demo workspace!
      </Typography>
      <Button
        component={RouterLink}
        to={`/workspaces/create?organisationId=${workspace.organisation.id}`}
      >
        Add Workspace
      </Button>
      <Button
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

export default SampleData
