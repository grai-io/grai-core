import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { render, waitFor, screen, act } from "testing"
import ConnectorSelect, { GET_CONNECTORS } from "./ConnectorSelect"

const onSelect = jest.fn()

test("renders", async () => {
  render(<ConnectorSelect onSelect={onSelect} />, { withRouter: true })

  await waitFor(() => {
    expect(screen.getAllByText("Hello World")).toBeTruthy()
  })
})

test("renders other", async () => {
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

  render(<ConnectorSelect onSelect={onSelect} />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("others")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByText("PostgreSQL")).toBeInTheDocument()
  })
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

  render(<ConnectorSelect onSelect={onSelect} />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("search", async () => {
  const user = userEvent.setup()

  render(<ConnectorSelect onSelect={() => {}} />, { withRouter: true })

  await waitFor(() => {
    expect(screen.getAllByText("Hello World")).toBeTruthy()
  })

  await act(
    async () => await user.type(screen.getByRole("textbox"), "PostgreSQL"),
  )

  await waitFor(() => {
    expect(screen.getAllByText("Hello World")).toBeTruthy()
  })
})

test("filter", async () => {
  const user = userEvent.setup()

  render(<ConnectorSelect onSelect={() => {}} />, { withRouter: true })

  await waitFor(() => {
    expect(screen.getAllByText("Hello World")).toBeTruthy()
  })

  await act(
    async () =>
      await user.click(screen.getByRole("tab", { name: /hello world/i })),
  )

  await waitFor(() => {
    expect(screen.getAllByText("Hello World")).toBeTruthy()
  })
})
