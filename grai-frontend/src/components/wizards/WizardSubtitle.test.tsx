import React from "react"
import { render, screen } from "testing"
import WizardSubtitle from "./WizardSubtitle"

test("renders", async () => {
  render(<WizardSubtitle />)
})

test("renders title", async () => {
  render(<WizardSubtitle title="Test Title" />)

  expect(screen.getByText("Test Title")).toBeInTheDocument()
})

test("renders title icon", async () => {
  render(<WizardSubtitle title="Test Title" icon="/images/file-icon.png" />)

  expect(screen.getByText("Test Title")).toBeInTheDocument()
})
