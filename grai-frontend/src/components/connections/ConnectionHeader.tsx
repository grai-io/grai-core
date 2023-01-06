import { ContentCopy, KeyboardBackspace } from "@mui/icons-material"
import {
  Box,
  Button,
  Divider,
  IconButton,
  Tooltip,
  Typography,
} from "@mui/material"
import RunStatus from "components/runs/RunStatus"
import React from "react"
import { Link, useParams } from "react-router-dom"
import ConnectionRefresh, {
  Connection as BaseConnection,
} from "./ConnectionRefresh"

interface Connection extends BaseConnection {
  name: string
}

type ConnectionHeaderProps = {
  connection: Connection
  onRefresh?: () => void
}

const ConnectionHeader: React.FC<ConnectionHeaderProps> = ({
  connection,
  onRefresh,
}) => {
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
          {connection.last_run && (
            <RunStatus run={connection.last_run} link sx={{ ml: 2 }} />
          )}
        </Box>
        <ConnectionRefresh connection={connection} onRefresh={onRefresh} />
      </Box>
      <Divider />
    </>
  )
}

export default ConnectionHeader
