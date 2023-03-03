import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import profileMock from "testing/profileMock"
import { GET_TABLES_AND_EDGES } from "components/tables/TableLineage"
import Table, { GET_TABLE } from "./Table"

export const tableMock = {
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
        table: {
          id: "1",
          namespace: "default",
          name: "Table1",
          display_name: "Table1",
          is_active: true,
          data_source: "test",
          metadata: {},
          columns: [
            {
              id: "1",
              name: "Column1",
              display_name: "Column1",
              requirements_edges: [],
              metadata: {},
            },
          ],
          source_tables: [
            {
              id: "2",
              name: "Table2",
              display_name: "Table2",
            },
          ],
          destination_tables: [
            {
              id: "3",
              name: "Table3",
              display_name: "Table3",
            },
          ],
        },
      },
    },
  },
}

const mocks = [profileMock, tableMock]

test("renders", async () => {
  render(<Table />, {
    mocks,
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Profile")).toBeInTheDocument()
  })
})

test("error", async () => {
  const mocks = [
    profileMock,
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
    profileMock,
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

  const mocks = [
    profileMock,
    tableMock,
    tableMock,
    {
      request: {
        query: GET_TABLES_AND_EDGES,
        variables: {
          organisationName: "",
          workspaceName: "",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            tables: [
              {
                id: "2",
                namespace: "default",
                name: "Table2",
                display_name: "Table2",
                data_source: "test",
                metadata: {},
                columns: [],
                source_tables: [
                  {
                    id: "1",
                    name: "Table1",
                    display_name: "Table1",
                  },
                ],
                destination_tables: [],
              },
            ],
            other_edges: [],
          },
        },
      },
    },
  ]

  render(<Table />, {
    mocks,
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getAllByText("Lineage")).toBeTruthy()
  })

  await act(
    async () => await user.click(screen.getByRole("tab", { name: /Lineage/i }))
  )

  await waitFor(() => {
    expect(screen.getByTestId("table-lineage")).toBeInTheDocument()
  })
})

test("expand all", async () => {
  const user = userEvent.setup()

  render(<Table />, {
    mocks,
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Profile")).toBeInTheDocument()
  })

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /Expand all rows/i }))
  )

  await act(
    async () =>
      await user.click(
        screen.getByRole("button", { name: /Collapse all rows/i })
      )
  )
})

test("click row", async () => {
  const user = userEvent.setup()

  render(<Table />, {
    mocks,
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Profile")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getAllByText("Table1")).toBeTruthy()
  })

  await act(
    async () =>
      await user.click(
        // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
        screen.getByTestId("columns-table").querySelectorAll("tbody > tr")[0]
      )
  )

  await act(
    async () =>
      await user.click(
        // eslint-disable-next-line testing-library/no-container, testing-library/no-node-access
        screen.getByTestId("columns-table").querySelectorAll("tbody > tr")[0]
      )
  )
})

test("search", async () => {
  const user = userEvent.setup()

  render(<Table />, {
    mocks,
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Profile")).toBeInTheDocument()
  })

  await act(async () => await user.type(screen.getByRole("textbox"), "Search"))
})
