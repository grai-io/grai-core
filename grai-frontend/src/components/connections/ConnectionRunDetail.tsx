import { Box, Stack, Tooltip, Typography } from "@mui/material"
import NodeDetailRow from "components/nodes/NodeDetailRow"
import RunStatus from "components/runs/RunStatus"
import { durationAgo } from "helpers/runDuration"
import { DateTime } from "luxon"
import React from "react"

interface Run {
  id: string
  status: string
  created_at: string
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
        <Tooltip
          title={DateTime.fromISO(run.created_at).toLocaleString(
            DateTime.DATETIME_FULL_WITH_SECONDS
          )}
        >
          <Typography variant="body2">
            Started {durationAgo(run.created_at)} ago
          </Typography>
        </Tooltip>
        <Box>
          <RunStatus run={run} size="small" link />
        </Box>
      </Stack>
    )}
  </NodeDetailRow>
)

export default ConnectionRunDetail
