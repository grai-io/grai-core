import React from "react"
import { KeyboardBackspace, ContentCopy } from "@mui/icons-material"
import {
  Box,
  Button,
  Typography,
  Tooltip,
  IconButton,
  Divider,
} from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import { Link } from "react-router-dom"
import ConnectionRun, {
  Connection as BaseConnection,
  RunResult,
} from "components/connections/ConnectionRun"
import RunStatus from "./RunStatus"

interface Connector {
  id: string
  name: string
}

interface Connection extends BaseConnection {
  id: string
  name: string
  connector: Connector
}

interface Run {
  id: string
  connection: Connection | null
  status: string
}

type RunHeaderProps = {
  run: Run
  workspaceId: string
}

const RunHeader: React.FC<RunHeaderProps> = ({ run, workspaceId }) => {
  const { routePrefix, workspaceNavigate } = useWorkspace()

  const handleRun = (run: RunResult) => workspaceNavigate(`runs/${run.id}`)

  return (
    <>
      <Box sx={{ display: "flex", p: 2 }}>
        <Box>
          <Button
            component={Link}
            to={
              run.connection
                ? `${routePrefix}/connections/${run.connection.id}`
                : `${routePrefix}/runs`
            }
            color="secondary"
            startIcon={<KeyboardBackspace />}
          >
            Back
          </Button>
        </Box>
        <Typography variant="h6" sx={{ mx: 1, mt: 0.3 }}>
          {run.connection ? `${run.connection.name}/` : null}
          {run.id.slice(0, 6)}
        </Typography>
        <Box>
          <Tooltip title="Copy Run id">
            <IconButton sx={{ mt: 0.5 }}>
              <ContentCopy sx={{ fontSize: 15 }} />
            </IconButton>
          </Tooltip>
        </Box>
        <RunStatus run={run} sx={{ ml: 2 }} />
        <Box sx={{ flexGrow: 1 }} />
        {run.connection && (
          <ConnectionRun
            connection={run.connection}
            workspaceId={workspaceId}
            onRun={handleRun}
          />
        )}
      </Box>
      <Divider />
    </>
  )
}

export default RunHeader
