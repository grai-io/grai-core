import React, { useEffect, useState } from "react"
import { Tooltip, Typography } from "@mui/material"
import { DateTime, Interval } from "luxon"
import { durationToString, runDurationString } from "helpers/runDuration"
import RunTimings, { Run } from "./RunTimings"

type RunDurationProps = {
  run: Run
}

const UpdatingDuration = (props: RunDurationProps) => {
  const { run } = props
  const [duration, setDuration] = useState<Interval | undefined>(undefined)

  useEffect(() => {
    let myInterval = setInterval(() => {
      const duration = Interval.fromDateTimes(
        run.started_at ? DateTime.fromISO(run.started_at) : DateTime.now(),
        run.finished_at ? DateTime.fromISO(run.finished_at) : DateTime.now()
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

const RunDuration: React.FC<RunDurationProps> = ({ run }) => {
  if (run.finished_at)
    return (
      <Tooltip title={<RunTimings run={run} />}>
        <Typography variant="body2">{runDurationString(run)}</Typography>
      </Tooltip>
    )

  return <UpdatingDuration run={run} />
}

export default RunDuration
