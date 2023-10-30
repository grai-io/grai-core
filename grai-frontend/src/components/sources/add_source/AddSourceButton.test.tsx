import React from "react"
import userEvent from "@testing-library/user-event"
import { act, render, screen, waitFor } from "testing"
import AddSourceButton from "./AddSourceButton"

const workspace = {
  id: "1",
  sample_data: false,
  organisation: {
    id: "1",
  },
}

const sampleWorkspace = {
  id: "1",
  sample_data: true,
  organisation: {
    id: "1",
  },
}

test("click standard", async () => {
  const user = userEvent.setup()

  render(<AddSourceButton workspace={workspace} />, {
    route: "/default/demo/sources",
    path: "/:organisationName/:workspaceName/sources",
    routes: ["/:organisationName/:workspaceName/connections/create"],
  })

  expect(screen.getByRole("link", { name: /add source/i })).toBeInTheDocument()

  await act(async () => await user.click(screen.getByRole("link")))

  await screen.findByText("New Page")
})

test("click sample", async () => {
  const user = userEvent.setup()

  render(<AddSourceButton workspace={sampleWorkspace} />, {
    route: "/default/demo/sources",
    path: "/:organisationName/:workspaceName/sources",
    routes: ["/:organisationName/:workspaceName/connections/create"],
  })

  expect(
    screen.getByRole("button", { name: /add source/i }),
  ).toBeInTheDocument()

  await act(async () => await user.click(screen.getByRole("button")))

  await screen.findByText("You are currently in a demo workspace.")

  expect(screen.getByRole("link", { name: /add source/i })).toBeInTheDocument()

  await act(
    async () =>
      await user.click(screen.getByRole("link", { name: /add source/i })),
  )

  await screen.findByText("New Page")
})

test("click sample workspace", async () => {
  const user = userEvent.setup()

  render(<AddSourceButton workspace={sampleWorkspace} />, {
    route: "/default/demo/sources",
    path: "/:organisationName/:workspaceName/sources",
    routes: ["/workspaces/create"],
  })

  expect(
    screen.getByRole("button", { name: /add source/i }),
  ).toBeInTheDocument()

  await act(async () => await user.click(screen.getByRole("button")))

  await screen.findByText("You are currently in a demo workspace.")

  expect(
    screen.getByRole("link", { name: /add workspace/i }),
  ).toBeInTheDocument()

  await act(
    async () =>
      await user.click(screen.getByRole("link", { name: /add workspace/i })),
  )

  await screen.findByText("New Page")
})

test("cancel", async () => {
  const user = userEvent.setup()

  render(<AddSourceButton workspace={sampleWorkspace} />, {
    route: "/default/demo/sources",
    path: "/:organisationName/:workspaceName/sources",
    routes: ["/:organisationName/:workspaceName/connections/create"],
  })

  expect(
    screen.getByRole("button", { name: /add source/i }),
  ).toBeInTheDocument()

  await act(async () => await user.click(screen.getByRole("button")))

  await screen.findByText("You are currently in a demo workspace.")

  expect(screen.getByRole("link", { name: /add source/i })).toBeInTheDocument()

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /cancel/i })),
  )

  await waitFor(() =>
    expect(
      screen.queryByText("You are currently in a demo workspace."),
    ).not.toBeInTheDocument(),
  )
})
