import { Refresh } from "@mui/icons-material"
import { MenuItem, ListItemIcon, ListItemText, Button } from "@mui/material"
import React from "react"

interface Connection {
  id: string
}

type ConnectionRefreshProps = {
  connection: Connection
  menuItem?: boolean
  disabled?: boolean
}

const ConnectionRefresh: React.FC<ConnectionRefreshProps> = ({
  menuItem,
  disabled,
}) => {
  if (menuItem)
    return (
      <MenuItem disabled={disabled}>
        <ListItemIcon>
          <Refresh />
        </ListItemIcon>
        <ListItemText primary="Refresh" />
      </MenuItem>
    )

  return (
    <Button
      variant="outlined"
      startIcon={<Refresh />}
      disabled={disabled}
      data-testid="connection-refresh"
    >
      Refresh
    </Button>
  )
}

export default ConnectionRefresh
