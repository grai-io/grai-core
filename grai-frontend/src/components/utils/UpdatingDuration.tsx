import React, { ReactNode, useEffect, useState } from "react"
import { Tooltip, Typography } from "@mui/material"
import { DateTime, Interval } from "luxon"
import { durationToString } from "helpers/runDuration"

type UpdatingDurationProps = {
  start: string | null
  end?: string | null
  tooltip?: string | ReactNode
  length?: number
  long?: boolean
}

const fetchDuration = (start: string | null, end?: string | null) =>
  Interval.fromDateTimes(
    start ? DateTime.fromISO(start) : DateTime.now(),
    end ? DateTime.fromISO(end) : DateTime.now()
  )

const UpdatingDuration: React.FC<UpdatingDurationProps> = ({
  start,
  end,
  tooltip,
  length,
  long,
}) => {
  const [duration, setDuration] = useState<Interval>(fetchDuration(start, end))

  useEffect(() => {
    let myInterval = setInterval(
      () => setDuration(fetchDuration(start, end)),
      1000
    )

    return () => {
      clearInterval(myInterval)
    }
  }, [duration, setDuration, start, end])

  const durationString = durationToString(
    duration
      .toDuration(["years", "months", "days", "hours", "minutes", "seconds"])
      .toObject(),
    length,
    long
  )

  return (
    <Tooltip arrow title={tooltip}>
      <Typography variant="body2">{durationString}</Typography>
    </Tooltip>
  )
}

export default UpdatingDuration
