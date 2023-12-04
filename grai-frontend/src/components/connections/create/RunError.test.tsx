import { render, screen } from "testing"
import RunError from "./RunError"

test("renders", async () => {
  const run = {
    id: "1",
    metadata: {},
  }

  render(<RunError run={run} />)

  expect(screen.getByText("Validation Failed - undefined")).toBeInTheDocument()
})

test("renders unknown", async () => {
  const run = {
    id: "1",
    metadata: {
      error: "Unknown",
    },
  }

  render(<RunError run={run} />)

  expect(screen.getByText("Validation Failed")).toBeInTheDocument()
})

test("renders no connection", async () => {
  const run = {
    id: "1",
    metadata: {
      error: "No connection",
    },
  }

  render(<RunError run={run} />)

  expect(
    screen.getByText("Validation Failed - No connection"),
  ).toBeInTheDocument()
  expect(
    screen.getByText(
      "You may need to whitelist the Grai Cloud IP address, see",
    ),
  ).toBeInTheDocument()
})
