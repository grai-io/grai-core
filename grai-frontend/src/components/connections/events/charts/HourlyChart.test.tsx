import React from "react"
import { render, screen, waitFor } from "testing"
import HourlyChart from "./HourlyChart"
import { DateTime } from "luxon"

const events = [
  {
    status: "success",
    date: DateTime.now().toISO() as string,
  },
  {
    status: "error",
    date: DateTime.now().toISO() as string,
  },
]

test("renders", async () => {
  render(<HourlyChart events={events} responsive={false} />)
})

test("renders empty", async () => {
  render(<HourlyChart events={[]} responsive={false} />)
})
