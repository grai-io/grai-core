import userEvent from "@testing-library/user-event"
import { act, render, screen } from "testing"
import ConnectorCard from "./ConnectorCard"

test("renders", async () => {
  render(
    <ConnectorCard
      connector={{
        id: "1",
        name: "connector 1",
        metadata: null,
        icon: null,
      }}
    />,
    {
      withRouter: true,
    },
  )
})

test("coming soon", async () => {
  render(
    <ConnectorCard
      connector={{
        id: "1",
        name: "connector 1",
        metadata: null,
        status: "coming_soon",
        icon: null,
      }}
    />,
    {
      withRouter: true,
    },
  )

  expect(screen.getByText(/Coming soon/i)).toBeInTheDocument()
})

test("alpha", async () => {
  render(
    <ConnectorCard
      connector={{
        id: "1",
        name: "connector 1",
        metadata: null,
        status: "alpha",
        icon: null,
      }}
    />,
    {
      withRouter: true,
    },
  )

  expect(screen.getByText(/alpha/i)).toBeInTheDocument()
})

test("click", async () => {
  const user = userEvent.setup()

  render(
    <ConnectorCard
      connector={{
        id: "1",
        name: "connector 1",
        metadata: null,
        icon: null,
      }}
    />,
    {
      withRouter: true,
      routes: ["/:organisationName/:workspaceName/connections/create"],
    },
  )

  await act(async () => {
    await user.click(screen.getByText("connector 1"))
  })

  await screen.findByText("New Page")
})

test("to", async () => {
  const user = userEvent.setup()

  render(
    <ConnectorCard
      connector={{
        id: "1",
        name: "connector 1",
        metadata: null,
        to: "a",
        icon: null,
      }}
    />,
    {
      withRouter: true,
      routes: ["/a"],
    },
  )

  await act(async () => {
    await user.click(screen.getByText("connector 1"))
  })

  await screen.findByText("New Page")
})
