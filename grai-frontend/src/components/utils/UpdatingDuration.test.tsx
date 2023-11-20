import { render } from "@testing-library/react"
import UpdatingDuration from "./UpdatingDuration"

const start = "2021-01-01T00:00:00"
const end = "2021-01-01T01:00:00"

beforeEach(() => {
  jest.useFakeTimers()
})

test("renders", async () => {
  render(<UpdatingDuration start={start} end={end} />)

  jest.runOnlyPendingTimers()
})

test("renders no end", async () => {
  render(<UpdatingDuration start={start} />)

  jest.runOnlyPendingTimers()
})

afterEach(() => {
  jest.runOnlyPendingTimers()
  jest.useRealTimers()
})
