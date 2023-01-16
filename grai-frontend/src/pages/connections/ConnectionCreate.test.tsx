import React from "react"
import { renderWithRouter, screen } from "testing"
import ConnectionCreate from "./ConnectionCreate"

test("renders", async () => {
  renderWithRouter(<ConnectionCreate />)

  expect(screen.getByText("Create Connection")).toBeTruthy()
  expect(screen.getByText("Select a connector")).toBeTruthy()
})
