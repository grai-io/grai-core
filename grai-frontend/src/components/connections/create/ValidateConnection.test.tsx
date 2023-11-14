import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import ValidateConnection, { GET_RUN } from "./ValidateConnection"

const onValidate = jest.fn()

test("renders", async () => {
  render(
    <ValidateConnection
      workspaceId="1"
      run={{
        id: "1",
      }}
      onValidate={onValidate}
    />,
  )
})

test("error result", async () => {
  const mocks = [
    {
      request: {
        query: GET_RUN,
        variables: {
          workspaceId: "1",
          runId: "1",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            run: {
              id: "1",
              status: "error",
              metadata: {
                error: "Run Error",
                message: "Error Message",
              },
              connection: {
                id: "1",
                validated: false,
              },
            },
          },
        },
      },
    },
  ]

  render(
    <ValidateConnection
      workspaceId="1"
      run={{
        id: "1",
      }}
      onValidate={onValidate}
    />,
    { mocks },
  )

  await waitFor(() => {
    expect(
      screen.getByText("Validation Failed - Run Error"),
    ).toBeInTheDocument()
  })

  expect(screen.getByText("Error Message")).toBeInTheDocument()
})

test("error result unknown", async () => {
  const mocks = [
    {
      request: {
        query: GET_RUN,
        variables: {
          workspaceId: "1",
          runId: "1",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            run: {
              id: "1",
              status: "error",
              metadata: {
                error: "Unknown",
                message: "Error Message",
              },
              connection: {
                id: "1",
                validated: false,
              },
            },
          },
        },
      },
    },
  ]

  render(
    <ValidateConnection
      workspaceId="1"
      run={{
        id: "1",
      }}
      onValidate={onValidate}
    />,
    { mocks },
  )

  await waitFor(() => {
    expect(screen.getByText("Validation Failed")).toBeInTheDocument()
  })

  expect(screen.getByText("Error Message")).toBeInTheDocument()
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_RUN,
        variables: {
          workspaceId: "1",
          runId: "1",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(
    <ValidateConnection
      workspaceId="1"
      run={{
        id: "1",
      }}
      onValidate={onValidate}
    />,
    { mocks },
  )

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
