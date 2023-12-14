import React from "react"
import { Alert, AlertTitle, Link, Typography } from "@mui/material"

interface Run {
  id: string
  status?: string
  metadata?: any
}

type RunErrorProps = {
  run: Run
}

const RunError: React.FC<RunErrorProps> = ({ run }) => (
  <Alert severity="error" sx={{ mt: 2 }}>
    <AlertTitle>
      Validation Failed
      {run.metadata.error !== "Unknown" ? ` - ${run.metadata.error}` : ""}
    </AlertTitle>
    {run.metadata.message}
    {run.metadata.error === "No connection" && (
      <Typography variant="body2" sx={{ mt: 1 }}>
        You may need to whitelist the Grai Cloud IP address, see{" "}
        <Link
          href="https://docs.grai.io/cloud/security/ip_whitelisting"
          target="_blank"
        >
          IP Whitelisting
        </Link>
      </Typography>
    )}
  </Alert>
)

export default RunError
