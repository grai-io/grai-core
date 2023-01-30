import runPolling from "./runPolling"

const startPolling = jest.fn()
const stopPolling = jest.fn()

test("runDuration queued", () => {
  expect(runPolling("queued", startPolling, stopPolling)()).toBeUndefined()

  expect(startPolling).toHaveBeenCalled()
})

test("runDuration running", () => {
  expect(runPolling("running", startPolling, stopPolling)()).toBeUndefined()

  expect(startPolling).toHaveBeenCalled()
})

test("runDuration success", () => {
  expect(runPolling("success", startPolling, stopPolling)()).toBeUndefined()

  expect(stopPolling).toHaveBeenCalled()
})

test("runDuration error", () => {
  expect(runPolling("error", startPolling, stopPolling)()).toBeUndefined()

  expect(stopPolling).toHaveBeenCalled()
})
