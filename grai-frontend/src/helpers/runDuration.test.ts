import { DateTime, Interval } from "luxon"
import { runDuration, runDurationString } from "./runDuration"

test("runDuration", () =>
  expect(
    runDuration({
      started_at: "2021-01-01T01:00:00",
      finished_at: "2021-01-01T01:01:20",
    })
  ).toEqual(
    Interval.fromDateTimes(
      DateTime.fromISO("2021-01-01T01:00:00"),
      DateTime.fromISO("2021-01-01T01:01:20")
    )
  ))

test("runDurationString", () =>
  expect(
    runDurationString({
      started_at: "2021-01-01T01:00:00",
      finished_at: "2021-01-01T01:01:01",
    })
  ).toEqual("1m 1s"))

test("runDurationString minutes", () =>
  expect(
    runDurationString({
      started_at: "2021-01-01T01:00:00",
      finished_at: "2021-01-01T01:02:00",
    })
  ).toEqual("2m"))

test("runDurationString seconds", () =>
  expect(
    runDurationString({
      started_at: "2021-01-01T01:00:00",
      finished_at: "2021-01-01T01:00:35",
    })
  ).toEqual("35s"))

test("runDurationString zero", () =>
  expect(
    runDurationString({
      started_at: "2021-01-01T01:00:00",
      finished_at: "2021-01-01T01:00:00",
    })
  ).toEqual("0s"))
