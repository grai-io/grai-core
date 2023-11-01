import React from "react"
import { Box, Grid, Typography } from "@mui/material"
import ClearWorkspace from "./ClearWorkspace"
import ClearWorkspaceCache from "./ClearWorkspaceCache"
import HideDemoWorkspace from "./HideDemoWorkspace"

export interface Workspace {
  id: string
  name: string
  sample_data: boolean
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
        {workspace.sample_data && <HideDemoWorkspace workspace={workspace} />}
        <ClearWorkspace workspace={workspace} />
      </Grid>
    </Grid>
  </Box>
)

export default WorkspaceDanger
