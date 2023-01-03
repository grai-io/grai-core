import { ContentCopy, KeyboardBackspace } from "@mui/icons-material"
import {
  Box,
  Button,
  Divider,
  IconButton,
  Tooltip,
  Typography,
} from "@mui/material"
import React from "react"
import { Link, useParams } from "react-router-dom"
import ConnectionRefresh from "./ConnectionRefresh"

interface Run {
  id: string
  status: string
}

interface Connection {
  id: string
  name: string
  last_run: Run | null
}

type ConnectionHeaderProps = {
  connection: Connection
}

const ConnectionHeader: React.FC<ConnectionHeaderProps> = ({ connection }) => {
  const { workspaceId } = useParams()

  return (
    <>
      <Box sx={{ display: "flex", p: 2 }}>
        <Box>
          <Button
            component={Link}
            to={`/workspaces/${workspaceId}/connections`}
            color="secondary"
            startIcon={<KeyboardBackspace />}
          >
            Back
          </Button>
        </Box>
        <Typography
          variant="h6"
          sx={{ textTransform: "uppercase", mx: 1, mt: 0.3 }}
        >
          {connection.name}
        </Typography>
        <Box sx={{ flexGrow: 1 }}>
          <Tooltip title="Copy Connection Name">
            <IconButton sx={{ mt: 0.5 }}>
              <ContentCopy sx={{ fontSize: 15 }} />
            </IconButton>
          </Tooltip>
        </Box>
        <ConnectionRefresh connection={connection} />
      </Box>
      <Divider />
    </>
  )
}

export default ConnectionHeader
