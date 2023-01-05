import { DateTime, DurationObjectUnits, Interval } from "luxon"

interface Run {
  started_at: string | null
  finished_at: string | null
}

interface RunWithQueuedAt extends Run {
  created_at: string
}

export const runDuration = (run: Run) =>
  Interval.fromDateTimes(
    run.started_at ? DateTime.fromISO(run.started_at) : DateTime.now(),
    run.finished_at ? DateTime.fromISO(run.finished_at) : DateTime.now()
  )

export const runQueued = (run: RunWithQueuedAt) =>
  Interval.fromDateTimes(
    DateTime.fromISO(run.created_at),
    run.started_at ? DateTime.fromISO(run.started_at) : DateTime.now()
  )

export const durationToString = (
  duration: DurationObjectUnits,
  length: number = 2
) => {
  if (
    (duration.years ?? 0) +
      (duration.months ?? 0) +
      (duration.days ?? 0) +
      (duration.hours ?? 0) +
      (duration.minutes ?? 0) +
      (duration.seconds ?? 0) ===
    0
  )
    return "0s"

  let res: string[] = []

  if (duration.years) res.push(`${duration.years}yr`)
  if (duration.months) res.push(`${duration.months}mo`)
  if (duration.days) res.push(`${Math.round(duration.days)}d`)
  if (duration.hours) res.push(`${duration.hours}h`)
  if (duration.minutes) res.push(`${duration.minutes}m`)
  if (duration.seconds) res.push(`${Math.round(duration.seconds)}s`)

  return res.slice(0, length).join(" ")
}

export const durationAgo = (input: DateTime | string, length: number = 2) =>
  durationToString(
    Interval.fromDateTimes(
      typeof input === "string" ? DateTime.fromISO(input) : input,
      DateTime.now()
    )
      .toDuration(["years", "months", "days", "hours", "minutes", "seconds"])
      .toObject()
  )

export const runDurationString = (run: Run): string =>
  durationToString(
    runDuration(run).toDuration(["hours", "minutes", "seconds"]).toObject()
  )

export const runQueuedString = (run: RunWithQueuedAt): string =>
  durationToString(
    runQueued(run).toDuration(["hours", "minutes", "seconds"]).toObject()
  )
