import React from "react"
import { ContentCopy, KeyboardBackspace } from "@mui/icons-material"
import {
  Box,
  Button,
  Divider,
  IconButton,
  Tooltip,
  Typography,
} from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import { Link } from "react-router-dom"
import RunStatus from "components/runs/RunStatus"
import ConnectionRun, { Connection as BaseConnection } from "./ConnectionRun"

interface Connection extends BaseConnection {
  name: string
}

type ConnectionHeaderProps = {
  connection: Connection
  workspaceId: string
  onRun?: () => void
}

const ConnectionHeader: React.FC<ConnectionHeaderProps> = ({
  connection,
  workspaceId,
  onRun,
}) => {
  const { routePrefix } = useWorkspace()

  return (
    <>
      <Box sx={{ display: "flex", p: 2 }}>
        <Box>
          <Button
            component={Link}
            to={`${routePrefix}/connections`}
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
        <ConnectionRun
          connection={connection}
          workspaceId={workspaceId}
          onRun={onRun}
        />
      </Box>
      <Divider />
    </>
  )
}

export default ConnectionHeader
