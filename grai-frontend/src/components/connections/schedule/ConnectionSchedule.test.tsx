import { Table, TableBody } from "@mui/material"
import { render, screen } from "testing"
import ConnectionSchedule from "./ConnectionSchedule"

test("renders", async () => {
  const connection = {
    id: "1",
    schedules: null,
    is_active: false,
    namespace: "default",
    name: "c1",
    metadata: {},
    connector: {
      id: "1",
      name: "c1",
      metadata: null,
    },
  }

  render(
    <Table>
      <TableBody>
        <ConnectionSchedule connection={connection} />
      </TableBody>
    </Table>
  )

  expect(screen.getByText("Schedule")).toBeInTheDocument()
})

test("renders cron", async () => {
  const connection = {
    id: "1",
    is_active: false,
    namespace: "default",
    name: "c1",
    metadata: null,
    schedules: {
      type: "cron",
      cron: {
        minutes: "*",
        hours: "*",
        day_of_week: "*",
        day_of_month: "*",
        month_of_year: "*",
      },
    },
    connector: {
      id: "1",
      name: "c1",
      metadata: null,
    },
  }

  render(
    <Table>
      <TableBody>
        <ConnectionSchedule connection={connection} />
      </TableBody>
    </Table>
  )

  expect(screen.getByText("Schedule")).toBeInTheDocument()
})
