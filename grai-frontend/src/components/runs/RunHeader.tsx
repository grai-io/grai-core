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
import React from "react"
import { Link } from "react-router-dom"
import RunStatus from "./RunStatus"

interface Connector {
  id: string
  name: string
}

interface Connection {
  id: string
  name: string
}

interface Run {
  id: string
  connector: Connector
  connection: Connection | null
  status: string
}

type RunHeaderProps = {
  run: Run
}

const RunHeader: React.FC<RunHeaderProps> = ({ run }) => {
  const { routePrefix } = useWorkspace()

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
        <Typography
          variant="h6"
          sx={{ textTransform: "uppercase", mx: 1, mt: 0.3 }}
        >
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
      </Box>
      <Divider />
    </>
  )
}

export default RunHeader
