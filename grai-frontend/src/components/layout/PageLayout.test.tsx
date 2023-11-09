import { render, screen } from "testing"
import PageLayout from "./PageLayout"

test("renders", async () => {
  render(<PageLayout>Test</PageLayout>, { withRouter: true })

  expect(screen.getByText("Test")).toBeInTheDocument()
})

test("getting started", async () => {
  render(<PageLayout gettingStarted>Test</PageLayout>, { withRouter: true })

  expect(screen.getByText("Test")).toBeInTheDocument()
})

test("sample data", async () => {
  const workspace = {
    organisation: {
      id: "1",
    },
  }

  render(
    <PageLayout sampleData workspace={workspace}>
      Test
    </PageLayout>,
    { withRouter: true },
  )

  expect(screen.getByText("Test")).toBeInTheDocument()
  expect(
    screen.getByText("Welcome to your demo workspace!"),
  ).toBeInTheDocument()
})
