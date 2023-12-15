import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { render, screen, act } from "testing"
import ConnectorSelect, { GET_CONNECTORS } from "./ConnectorSelect"

test("renders", async () => {
  render(<ConnectorSelect />, { withRouter: true })

  await screen.findAllByText("Hello World")
})

test("renders other", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: GET_CONNECTORS,
      },
      result: {
        data: {
          connectors: [
            {
              id: "1",
              priority: 1,
              name: "PostgreSQL",
              category: null,
              status: "general_release",
              icon: "",
              metadata: {
                fields: [
                  {
                    name: "dbname",
                    label: "Database Name",
                    required: true,
                  },
                  {
                    name: "user",
                    required: true,
                  },
                  {
                    name: "password",
                    secret: true,
                    required: true,
                  },
                  {
                    name: "host",
                    required: true,
                  },
                  {
                    name: "port",
                    default: 5432,
                    required: true,
                  },
                ],
              },
            },
            {
              id: "2",
              priority: 2,
              name: "Data Tool",
              category: "data tools",
              status: "coming_soon",
              icon: "",
              metadata: {},
            },
          ],
        },
      },
    },
  ]

  render(<ConnectorSelect />, { mocks, withRouter: true })

  await screen.findByText("Others")

  await act(async () => {
    await user.click(screen.getByText("Others"))
  })

  await screen.findByText("PostgreSQL")
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_CONNECTORS,
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<ConnectorSelect />, { mocks, withRouter: true })

  await screen.findByText("Error!")
})

test("search", async () => {
  const user = userEvent.setup()

  render(<ConnectorSelect />, { withRouter: true })

  await screen.findAllByText("Hello World")

  await act(
    async () => await user.type(screen.getByRole("textbox"), "PostgreSQL"),
  )

  await screen.findAllByText("Hello World")
})

test("filter", async () => {
  const user = userEvent.setup()

  render(<ConnectorSelect />, { withRouter: true })

  await screen.findAllByText("Hello World")

  await act(
    async () =>
      await user.click(screen.getByRole("tab", { name: /hello world/i })),
  )

  await screen.findAllByText("Hello World")
})
