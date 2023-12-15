import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, fireEvent, render, screen } from "testing"
import CreateAlertDialog, { CREATE_ALERT } from "./CreateAlertDialog"

const onClose = jest.fn()

test("renders", async () => {
  render(<CreateAlertDialog workspaceId="1" open={true} onClose={onClose} />, {
    withRouter: true,
  })

  await screen.findByText("Add alert")
})

test("submit", async () => {
  const user = userEvent.setup()

  render(<CreateAlertDialog workspaceId="1" open={true} onClose={onClose} />, {
    withRouter: true,
  })

  await screen.findByText("Add alert")

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: /name/i }),
        "Test Alert",
      ),
  )

  fireEvent.change(screen.getByTestId("channel-select"), {
    target: { value: "email" },
  })

  await act(
    async () =>
      await user.type(
        screen.getByRole("combobox", { name: "" }),
        "email@grai.io",
      ),
  )

  await act(async () => await user.keyboard("{enter}"))

  await act(async () => await user.click(screen.getByRole("checkbox")))

  await act(
    async () => await user.click(screen.getByRole("button", { name: /Save/i })),
  )
})

test("error", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: CREATE_ALERT,
        variables: {
          workspaceId: "1",
          name: "Test Alert",
          // channel: "",
          // channel_metadata: {},
          channel: "email",
          channel_metadata: {
            emails: ["email@grai.io"],
          },
          triggers: {},
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<CreateAlertDialog workspaceId="1" open={true} onClose={onClose} />, {
    mocks,
  })

  await screen.findByText("Add alert")

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: /name/i }),
        "Test Alert",
      ),
  )

  fireEvent.change(screen.getByTestId("channel-select"), {
    target: { value: "email" },
  })

  await act(
    async () =>
      await user.type(
        screen.getByRole("combobox", { name: "" }),
        "email@grai.io",
      ),
  )

  await act(async () => await user.keyboard("{enter}"))

  await act(
    async () => await user.click(screen.getByRole("button", { name: /Save/i })),
  )

  await screen.findByText("Error!")
})
