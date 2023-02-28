import React from "react"
import { Alert, AlertTitle, Typography, Box } from "@mui/material"

type WorkspaceNotFoundProps = {
  organisationName: string
  workspaceName: string
}

const WorkspaceNotFound: React.FC<WorkspaceNotFoundProps> = ({
  organisationName,
  workspaceName,
}) => (
  <Alert severity="error">
    <AlertTitle>Error</AlertTitle>
    <Typography variant="body2" sx={{ mb: 1 }}>
      Workspace{" "}
      <Box
        component="span"
        sx={{
          fontWeight: 800,
        }}
      >
        {organisationName}\{workspaceName}
      </Box>{" "}
      not found
    </Typography>
    <Typography variant="body2">Please contact your administrator</Typography>
  </Alert>
)

export default WorkspaceNotFound
