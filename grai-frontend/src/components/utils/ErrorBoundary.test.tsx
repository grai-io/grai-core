import { render, screen } from "testing"
import ErrorBoundary from "./ErrorBoundary"

test("renders", async () => {
  render(<ErrorBoundary>Result</ErrorBoundary>)

  expect(screen.getByText("Result")).toBeInTheDocument()
})

test("errors", async () => {
  const Child = () => {
    throw new Error()
  }

  render(
    <ErrorBoundary>
      <Child />
    </ErrorBoundary>
  )

  expect(screen.getByText("Sorry there was an error")).toBeInTheDocument()
})
