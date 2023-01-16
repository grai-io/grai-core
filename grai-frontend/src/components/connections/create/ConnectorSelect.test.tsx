import { GraphQLError } from "graphql"
import React from "react"
import { render, waitFor, screen, renderWithMocks } from "testing"
import ConnectorSelect, { GET_CONNECTORS } from "./ConnectorSelect"

test("renders", async () => {
  render(<ConnectorSelect onSelect={() => {}} />)

  await waitFor(() => {
    expect(screen.getAllByText("Hello World")).toBeTruthy()
  })
})

test("renders other", async () => {
  const mock = {
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
  }

  renderWithMocks(<ConnectorSelect onSelect={() => {}} />, [mock])

  await waitFor(() => {
    expect(screen.getByText("other")).toBeTruthy()
  })

  await waitFor(() => {
    expect(screen.getByText("PostgreSQL")).toBeTruthy()
  })
})

test("error", async () => {
  const mock = {
    request: {
      query: GET_CONNECTORS,
    },
    result: {
      errors: [new GraphQLError("Error!")],
    },
  }

  renderWithMocks(<ConnectorSelect onSelect={() => {}} />, [mock])

  await waitFor(() => {
    expect(screen.getAllByText("Error!")).toBeTruthy()
  })
})
