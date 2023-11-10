import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import Runs, { GET_RUNS } from "./Runs"

test("renders", async () => {
  render(<Runs />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: "Runs" })).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getAllByText("Hello World")).toBeTruthy()
  })
})

test("refresh", async () => {
  const user = userEvent.setup()

  render(<Runs />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: "Runs" })).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getAllByText("Hello World")).toBeTruthy()
  })

  await act(async () => await user.click(screen.getByTestId("RefreshIcon")))
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_RUNS,
        variables: {
          organisationName: "",
          workspaceName: "",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<Runs />, {
    withRouter: true,
    mocks,
  })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("search", async () => {
  const user = userEvent.setup()

  render(<Runs />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getAllByText("Hello World")).toBeTruthy()
  })

  await act(async () => await user.type(screen.getByRole("textbox"), "Search"))

  await waitFor(() => {
    expect(screen.getByRole("textbox")).toHaveValue("Search")
  })

  await waitFor(() => {
    expect(screen.getByText("No runs found")).toBeInTheDocument()
  })
})
