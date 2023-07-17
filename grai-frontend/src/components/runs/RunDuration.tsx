import React from "react"
import { Tooltip, Typography } from "@mui/material"
import { runDurationString } from "helpers/runDuration"
import UpdatingDuration from "components/utils/UpdatingDuration"
import RunTimings, { Run } from "./RunTimings"

type RunDurationProps = {
  run: Run
}

const RunDuration: React.FC<RunDurationProps> = ({ run }) => {
  if (run.finished_at)
    return (
      <Tooltip title={<RunTimings run={run} />}>
        <Typography variant="body2">{runDurationString(run)}</Typography>
      </Tooltip>
    )

  return (
    <UpdatingDuration
      start={run.started_at}
      end={run.finished_at}
      tooltip={<RunTimings run={run} />}
    />
  )
}

export default RunDuration
