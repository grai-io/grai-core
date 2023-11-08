import { render, screen } from "testing"
import WizardSubtitle from "./WizardSubtitle"

test("renders", async () => {
  render(<WizardSubtitle />)
})

test("renders title", async () => {
  render(<WizardSubtitle title="Test Title" />)

  expect(screen.getByText("Test Title")).toBeInTheDocument()
})

test("renders title subTitle", async () => {
  render(<WizardSubtitle title="Test Title" subTitle="Test subTitle" />)

  expect(screen.getByText("Test Title")).toBeInTheDocument()
  expect(screen.getByText("Test subTitle")).toBeInTheDocument()
})
