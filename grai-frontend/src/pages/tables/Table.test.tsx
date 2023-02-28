import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import Table, { GET_TABLE } from "./Table"

test("renders", async () => {
  render(<Table />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Profile")).toBeInTheDocument()
  })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_TABLE,
        variables: {
          organisationName: "",
          workspaceName: "",
          tableId: "",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<Table />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("not found", async () => {
  const mocks = [
    {
      request: {
        query: GET_TABLE,
        variables: {
          organisationName: "",
          workspaceName: "",
          tableId: "",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            table: null,
            tables: [],
            other_edges: [],
          },
        },
      },
    },
  ]

  render(<Table />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getAllByText("Page not found")).toBeTruthy()
  })
})

test("lineage", async () => {
  const user = userEvent.setup()

  render(<Table />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getAllByText("Lineage")).toBeTruthy()
  })

  await user.click(screen.getByRole("tab", { name: /Lineage/i }))
})

test("expand all", async () => {
  render(<Table />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Profile")).toBeInTheDocument()
  })

  await userEvent.click(
    screen.getByRole("button", { name: /Expand all rows/i })
  )

  await userEvent.click(
    screen.getByRole("button", { name: /Collapse all rows/i })
  )
})

test("click row", async () => {
  const user = userEvent.setup()

  render(<Table />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Profile")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getAllByText("Hello World")).toBeTruthy()
  })

  await user.click(
    // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
    screen.getByTestId("columns-table").querySelectorAll("tbody > tr")[0]
  )

  await user.click(
    // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
    screen.getByTestId("columns-table").querySelectorAll("tbody > tr")[0]
  )
})

test("search", async () => {
  render(<Table />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Profile")).toBeInTheDocument()
  })

  await userEvent.type(screen.getByRole("textbox"), "Search")
})
