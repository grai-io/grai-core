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

interface Node {
  id: string
  display_name: string
}

type NodeHeaderProps = {
  node: Node
}

const NodeHeader: React.FC<NodeHeaderProps> = ({ node }) => {
  const { workspaceId } = useParams()

  return (
    <>
      <Box sx={{ display: "flex", p: 2 }}>
        <Box>
          <Button
            component={Link}
            to={`/workspaces/${workspaceId}/nodes`}
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
          {node?.display_name ?? node?.id}
        </Typography>
        <Box>
          <Tooltip title="Copy Table Name">
            <IconButton sx={{ mt: 0.5 }}>
              <ContentCopy sx={{ fontSize: 15 }} />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>
      <Divider />
    </>
  )
}

export default NodeHeader
