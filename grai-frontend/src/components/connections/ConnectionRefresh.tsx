import { Refresh } from "@mui/icons-material"
import { LoadingButton } from "@mui/lab"
import {
  MenuItem,
  ListItemIcon,
  ListItemText,
  CircularProgress,
} from "@mui/material"
import React from "react"

interface Run {
  id: string
  status: string
}

interface Connection {
  id: string
  last_run: Run | null
}

type ConnectionRefreshProps = {
  connection: Connection
  menuItem?: boolean
  disabled?: boolean
}

const ConnectionRefresh: React.FC<ConnectionRefreshProps> = ({
  connection,
  menuItem,
  disabled,
}) => {
  const loading = connection.last_run?.status
    ? ["queued", "running"].includes(connection.last_run.status)
    : false

  if (menuItem)
    return (
      <MenuItem disabled={disabled || loading}>
        <ListItemIcon>
          {loading ? <CircularProgress /> : <Refresh />}
        </ListItemIcon>
        <ListItemText primary="Refresh" />
      </MenuItem>
    )

  return (
    <LoadingButton
      variant="outlined"
      startIcon={<Refresh />}
      disabled={disabled}
      loading={loading}
      loadingPosition="start"
      data-testid="connection-refresh"
    >
      {loading ? connection.last_run?.status : "Refresh"}
    </LoadingButton>
  )
}

export default ConnectionRefresh
