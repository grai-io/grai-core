import React from "react"
import { render, screen } from "testing"
import DialogTitle from "./DialogTitle"

test("renders", async () => {
  render(<DialogTitle>Dialog Title Test</DialogTitle>)

  expect(screen.getByText("Dialog Title Test")).toBeInTheDocument()
})

test("renders with onClose", async () => {
  const handleClose = () => {}

  render(<DialogTitle onClose={handleClose}>Dialog Title Test</DialogTitle>)

  expect(screen.getByText("Dialog Title Test")).toBeInTheDocument()
})

test("renders with onBack", async () => {
  const handleBack = () => {}

  render(<DialogTitle onBack={handleBack}>Dialog Title Test</DialogTitle>)

  expect(screen.getByText("Dialog Title Test")).toBeInTheDocument()
})
