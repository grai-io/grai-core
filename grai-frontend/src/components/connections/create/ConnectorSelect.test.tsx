import React from "react"
import { GraphQLError } from "graphql"
import { render, waitFor, screen } from "testing"
import ConnectorSelect, { GET_CONNECTORS } from "./ConnectorSelect"

test("renders", async () => {
  render(<ConnectorSelect onSelect={() => {}} />)

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
              name: "PostgreSQL",
              category: null,
              coming_soon: false,
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
          ],
        },
      },
    },
  ]

  render(<ConnectorSelect onSelect={() => {}} />, { mocks })

  await waitFor(() => {
    expect(screen.getByText("other")).toBeInTheDocument()
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

  render(<ConnectorSelect onSelect={() => {}} />, { mocks })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
