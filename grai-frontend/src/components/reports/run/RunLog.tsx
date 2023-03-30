import React from "react"
import { Alert, AlertTitle, Typography } from "@mui/material"

interface RunMetadata {
  error?: string
}

export interface Run {
  id: string
  metadata: RunMetadata
}

type RunLogProps = {
  run: Run
}

const RunLog: React.FC<RunLogProps> = ({ run }) =>
  run.metadata.error ? (
    <Alert severity="error" sx={{ mt: 2 }}>
      <AlertTitle>Error</AlertTitle>
      {run.metadata.error.split("\n").map((line, index) => (
        <Typography variant="body2" key={index}>
          {line}
        </Typography>
      ))}
    </Alert>
  ) : null

export default RunLog
