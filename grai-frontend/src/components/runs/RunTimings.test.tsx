import { render, screen } from "testing"
import RunTimings from "./RunTimings"

test("renders", async () => {
  const run = {
    created_at: "2021-01-01T00:00:00",
    started_at: "2021-01-01T01:00:00",
    finished_at: "2021-01-01T02:00:00",
  }

  render(<RunTimings run={run} />, {
    withRouter: true,
  })

  expect(
    screen.getByText("January 1, 2021 at 12:00:00 AM GMT", {
      exact: false,
    })
  ).toBeInTheDocument()
})
