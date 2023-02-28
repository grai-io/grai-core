import React from "react"
import { Add, Refresh } from "@mui/icons-material"
import { Box, Button, Stack, Typography } from "@mui/material"
import { Link } from "react-router-dom"

type ConnectionsHeaderProps = {
  onRefresh?: () => void
}

const ConnectionsHeader: React.FC<ConnectionsHeaderProps> = ({ onRefresh }) => (
  <Box sx={{ m: 3, display: "flex" }}>
    <Typography variant="h4" sx={{ flexGrow: 1 }}>
      Connections
    </Typography>
    <Stack direction="row" spacing={1}>
      <Button
        variant="outlined"
        sx={{ minWidth: 0 }}
        onClick={onRefresh}
        size="small"
        data-testid="connection-refresh"
      >
        <Refresh />
      </Button>
      <Button
        variant="outlined"
        startIcon={<Add />}
        component={Link}
        to="create"
        size="small"
      >
        Add Connection
      </Button>
    </Stack>
  </Box>
)

export default ConnectionsHeader
