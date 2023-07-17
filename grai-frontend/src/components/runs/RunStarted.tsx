import { Tooltip, Typography } from "@mui/material"
import { durationToString } from "helpers/runDuration"
import { DateTime, Interval } from "luxon"
import React, { useEffect, useState } from "react"
import RunTimings, { Run } from "./RunTimings"

const getDuration = (run: Run) =>
  Interval.fromDateTimes(DateTime.fromISO(run.created_at), DateTime.now())

type RunStartedProps = {
  run: Run
}

const RunStarted: React.FC<RunStartedProps> = ({ run }) => {
  const [duration, setDuration] = useState<Interval | undefined>(
    getDuration(run)
  )

  useEffect(() => {
    let myInterval = setInterval(() => setDuration(getDuration(run)), 1000)

    return () => {
      clearInterval(myInterval)
    }
  }, [duration, setDuration, run])

  if (!duration) return null

  const durationString = durationToString(
    duration
      .toDuration(["years", "months", "days", "hours", "minutes", "seconds"])
      .toObject(),
    1,
    true
  )

  return (
    <Tooltip title={<RunTimings run={run} />}>
      <Typography variant="body2">{durationString} ago</Typography>
    </Tooltip>
  )
}

export default RunStarted
