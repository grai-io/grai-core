import React from "react"
import { renderWithRouter, screen, waitFor } from "testing"
import ConnectionCreate from "./ConnectionCreate"

test("renders", async () => {
  renderWithRouter(<ConnectionCreate />)

  await waitFor(() => {
    expect(screen.getByText("Create Connection")).toBeTruthy()
  })

  await waitFor(() => {
    expect(screen.queryByRole("progressbar")).toBeTruthy()
  })

  await waitFor(() => {
    expect(screen.queryByRole("progressbar")).toBeFalsy()
  })
})
