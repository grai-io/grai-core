import React from "react"
import { render, screen, waitFor } from "testing"
import DialogTitle from "./DialogTitle"

test("renders", async () => {
  render(<DialogTitle>Dialog Title Test</DialogTitle>)

  await waitFor(() => {
    expect(screen.getByText("Dialog Title Test")).toBeTruthy()
  })
})

test("renders with onClose", async () => {
  const handleClose = () => {}

  render(<DialogTitle onClose={handleClose}>Dialog Title Test</DialogTitle>)

  await waitFor(() => {
    expect(screen.getByText("Dialog Title Test")).toBeTruthy()
  })
})

test("renders with onBack", async () => {
  const handleBack = () => {}

  render(<DialogTitle onBack={handleBack}>Dialog Title Test</DialogTitle>)

  await waitFor(() => {
    expect(screen.getByText("Dialog Title Test")).toBeTruthy()
  })
})
