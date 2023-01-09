import { KeyboardBackspace, ContentCopy } from "@mui/icons-material"
import {
  Box,
  Button,
  Typography,
  Tooltip,
  IconButton,
  Divider,
} from "@mui/material"
import React from "react"
import { useParams, Link } from "react-router-dom"
import RunStatus from "./RunStatus"

interface Connection {
  id: string
  name: string
}

interface Run {
  id: string
  connection: Connection
  status: string
}

type RunHeaderProps = {
  run: Run
}

const RunHeader: React.FC<RunHeaderProps> = ({ run }) => {
  const { workspaceId } = useParams()

  return (
    <>
      <Box sx={{ display: "flex", p: 2 }}>
        <Box>
          <Button
            component={Link}
            to={`/workspaces/${workspaceId}/connections/${run.connection.id}`}
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
          {run.connection.name}/{run.id.slice(0, 6)}
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
