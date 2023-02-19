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

type Period = {
  short: string
  long: string
}

type PeriodText = { [k: string]: Period }

const periodText: PeriodText = {
  year: {
    short: "yr",
    long: "year",
  },
  month: {
    short: "mo",
    long: "month",
  },
  day: {
    short: "d",
    long: "day",
  },
  hour: {
    short: "h",
    long: "hour",
  },
  minute: {
    short: "m",
    long: "minute",
  },
  second: {
    short: "s",
    long: "second",
  },
}

const periodToText = (
  value: number,
  key: keyof PeriodText,
  long: boolean
): string =>
  long
    ? `${value} ${periodText[key].long}${value > 1 ? "s" : ""}`
    : `${value}${periodText[key].short}`

export const durationToString = (
  duration: DurationObjectUnits,
  length: number = 2,
  long: boolean = false
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

  if (duration.years) res.push(periodToText(duration.years, "year", long))
  if (duration.months) res.push(periodToText(duration.months, "month", long))
  if (duration.days) res.push(periodToText(duration.days, "day", long))
  if (duration.hours) res.push(periodToText(duration.hours, "hour", long))
  if (duration.minutes) res.push(periodToText(duration.minutes, "minute", long))
  if (duration.seconds)
    res.push(periodToText(Number(duration.seconds.toFixed(0)), "second", long))

  return res.slice(0, length).join(" ")
}

export const durationAgo = (
  input: DateTime | string,
  length: number = 2,
  long: boolean = true
) =>
  durationToString(
    Interval.fromDateTimes(
      typeof input === "string" ? DateTime.fromISO(input) : input,
      DateTime.now()
    )
      .toDuration(["years", "months", "days", "hours", "minutes", "seconds"])
      .toObject(),
    length,
    long
  )

export const runDurationString = (run: Run): string =>
  durationToString(
    runDuration(run).toDuration(["hours", "minutes", "seconds"]).toObject()
  )

export const runQueuedString = (run: RunWithQueuedAt): string =>
  durationToString(
    runQueued(run).toDuration(["hours", "minutes", "seconds"]).toObject()
  )
