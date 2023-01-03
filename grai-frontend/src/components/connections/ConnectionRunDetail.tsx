import { Box, Chip, Stack, Typography } from "@mui/material"
import NodeDetailRow from "components/nodes/NodeDetailRow"
import React from "react"

interface Run {
  id: string
  status: string
  started_at: string | null
}

type ConnectionRunDetailProps = {
  label: string
  run: Run | null
}

const ConnectionRunDetail: React.FC<ConnectionRunDetailProps> = ({
  label,
  run,
}) => (
  <NodeDetailRow label={label}>
    {run && (
      <Stack spacing={1}>
        <Typography variant="body2">{run?.started_at}</Typography>
        <Box>
          <Chip label={run?.status} />
        </Box>
      </Stack>
    )}
  </NodeDetailRow>
)

export default ConnectionRunDetail
