import { MoreHoriz } from "@mui/icons-material"
import { Box, Typography, Stack, Button } from "@mui/material"
import React from "react"
import ConnectionRefresh from "./ConnectionRefresh"

interface Connection {
  id: string
  name: string
}

type ConnectionHeaderProps = {
  connection: Connection
}

const ConnectionHeader: React.FC<ConnectionHeaderProps> = ({ connection }) => (
  <Box sx={{ display: "flex", p: 3 }}>
    <Typography variant="h4" sx={{ flexGrow: 1 }}>
      {connection.name}
    </Typography>
    <Stack direction="row" spacing={1}>
      <ConnectionRefresh connection={connection} />
      <Button variant="outlined" sx={{ minWidth: 0 }}>
        <MoreHoriz />
      </Button>
    </Stack>
  </Box>
)

export default ConnectionHeader
