import React from "react"
import { render, screen, waitFor } from "@testing-library/react"
import App from "./App"

jest.retryTimes(1)

test("renders", async () => {
  render(<App />)

  expect(screen.getByRole("progressbar")).toBeInTheDocument()

  await waitFor(() => {
    expect(screen.queryByRole("progressbar")).not.toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByText(/Welcome back!/i)).toBeInTheDocument()
  })
})
