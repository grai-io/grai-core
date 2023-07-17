import React from "react"
import { Tooltip, Typography } from "@mui/material"
import { runQueuedString } from "helpers/runDuration"
import UpdatingDuration from "components/utils/UpdatingDuration"
import RunTimings, { Run } from "./RunTimings"

type RunQueuedProps = {
  run: Run
}

const RunQueued: React.FC<RunQueuedProps> = ({ run }) => {
  if (run.started_at)
    return (
      <Tooltip title={<RunTimings run={run} />}>
        <Typography variant="body2">{runQueuedString(run)}</Typography>
      </Tooltip>
    )

  return (
    <UpdatingDuration
      start={run.created_at}
      end={run.started_at}
      tooltip={<RunTimings run={run} />}
    />
  )
}

export default RunQueued
