import React from "react"
import { render, screen, waitFor } from "@testing-library/react"
import App from "./App"

test("renders", async () => {
  render(<App />)

  expect(screen.getByRole("progressbar")).toBeInTheDocument()

  await waitFor(() => {
    expect(screen.getByText(/Welcome back!/i)).toBeInTheDocument()
  })
})
