import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import AlertConfiguration, { UPDATE_ALERT } from "./AlertConfiguration"

const alert = {
  id: "1",
  name: "Test Alert",
  channel: "email",
  channel_metadata: {},
  triggers: {},
  is_active: true,
  created_at: "1",
}

test("renders", async () => {
  render(<AlertConfiguration alert={alert} />, {
    withRouter: true,
  })

  await screen.findByRole("textbox", { name: /name/i })
})

test("submit", async () => {
  const user = userEvent.setup()

  render(<AlertConfiguration alert={alert} />, {
    routes: ["/:organisationName/:workspaceName/settings/alerts"],
  })

  await screen.findByRole("textbox", { name: /name/i })

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: /name/i }),
        "Test Alert2",
      ),
  )

  await act(
    async () => await user.type(screen.getByRole("combobox"), "email2@grai.io"),
  )

  await act(async () => await user.keyboard("{enter}"))

  await act(async () => await user.click(screen.getByRole("checkbox")))

  await act(
    async () => await user.click(screen.getByRole("button", { name: /Save/i })),
  )

  await screen.findByText("New Page")
})

test("error", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: UPDATE_ALERT,
        variables: {
          id: "1",
          name: "Test AlertTest Alert2",
          channel_metadata: { emails: ["email2@grai.io"] },
          triggers: { test_failure: true },
          is_active: true,
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<AlertConfiguration alert={alert} />, {
    mocks,
    withRouter: true,
  })

  await screen.findByRole("textbox", { name: /name/i })

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: /name/i }),
        "Test Alert2",
      ),
  )

  await waitFor(() =>
    expect(screen.getByRole("textbox", { name: /name/i })).toHaveValue(
      "Test AlertTest Alert2",
    ),
  )

  await act(
    async () => await user.type(screen.getByRole("combobox"), "email2@grai.io"),
  )

  await act(async () => await user.keyboard("{enter}"))

  await act(async () => await user.click(screen.getByRole("checkbox")))

  await act(
    async () => await user.click(screen.getByRole("button", { name: /Save/i })),
  )

  await screen.findByText("Error!")
})
