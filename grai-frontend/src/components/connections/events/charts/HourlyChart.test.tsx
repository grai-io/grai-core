import { DateTime } from "luxon"
import { render } from "testing"
import HourlyChart from "./HourlyChart"

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
