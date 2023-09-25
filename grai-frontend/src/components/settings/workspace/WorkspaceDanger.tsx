import React from "react"
import { Box, Grid, Typography } from "@mui/material"
import ClearWorkspace from "./ClearWorkspace"
import ClearWorkspaceCache from "./ClearWorkspaceCache"

export interface Workspace {
  id: string
  name: string
}

type WorkspaceDangerProps = {
  workspace: Workspace
}

const WorkspaceDanger: React.FC<WorkspaceDangerProps> = ({ workspace }) => (
  <Box sx={{ p: 3 }}>
    <Typography variant="h5" sx={{ mb: 3 }}>
      Danger Zone
    </Typography>
    <Grid container>
      <Grid item md={6}>
        <ClearWorkspaceCache />
        <ClearWorkspace workspace={workspace} />
      </Grid>
    </Grid>
  </Box>
)

export default WorkspaceDanger
