import React from "react"
import userEvent from "@testing-library/user-event"
import { act, render, screen, waitFor } from "testing"
import ConnectorCard from "./ConnectorCard"

const onSelect = jest.fn()

test("renders", async () => {
  render(
    <ConnectorCard
      connector={{
        id: "1",
        name: "connector 1",
        metadata: null,
      }}
      onSelect={onSelect}
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
      }}
      onSelect={onSelect}
    />,
    {
      withRouter: true,
    },
  )
})

test("click", async () => {
  const user = userEvent.setup()

  render(
    <ConnectorCard
      connector={{
        id: "1",
        name: "connector 1",
        metadata: null,
      }}
      onSelect={onSelect}
    />,
    {
      withRouter: true,
    },
  )

  await act(async () => {
    await user.click(screen.getByText("connector 1"))
  })

  expect(onSelect).toHaveBeenCalled()
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
      }}
      onSelect={onSelect}
    />,
    {
      withRouter: true,
      routes: ["/a"],
    },
  )

  await act(async () => {
    await user.click(screen.getByText("connector 1"))
  })

  await waitFor(() => {
    expect(screen.getByText("New Page")).toBeTruthy()
  })
})
