import { Tooltip, Typography } from "@mui/material"
import { durationToString, runQueuedString } from "helpers/runDuration"
import { DateTime, Interval } from "luxon"
import React, { useEffect, useState } from "react"
import RunTimings, { Run } from "./RunTimings"

type RunQueuedProps = {
  run: Run
}

const UpdatingDuration = (props: RunQueuedProps) => {
  const { run } = props
  const [duration, setDuration] = useState<Interval | undefined>(undefined)

  useEffect(() => {
    let myInterval = setInterval(() => {
      const duration = Interval.fromDateTimes(
        DateTime.fromISO(run.created_at),
        run.started_at ? DateTime.fromISO(run.started_at) : DateTime.now()
      )

      setDuration(duration)
    }, 1000)

    return () => {
      clearInterval(myInterval)
    }
  }, [duration, setDuration, run])

  if (!duration) return "-"

  const durationString = durationToString(
    duration
      .toDuration(["years", "months", "days", "hours", "minutes", "seconds"])
      .toObject()
  )

  return (
    <Tooltip arrow title={<RunTimings run={run} />}>
      <Typography variant="body2">{durationString}</Typography>
    </Tooltip>
  )
}

const RunQueued: React.FC<RunQueuedProps> = ({ run }) => {
  if (run.started_at)
    return (
      <Tooltip title={<RunTimings run={run} />}>
        <Typography variant="body2">{runQueuedString(run)}</Typography>
      </Tooltip>
    )

  return <UpdatingDuration run={run} />
}

export default RunQueued
