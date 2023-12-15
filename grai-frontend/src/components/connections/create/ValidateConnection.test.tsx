import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import ValidateConnection, { GET_RUN } from "./ValidateConnection"

const onSuccess = jest.fn()
const onFail = jest.fn()

test("renders success", async () => {
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
              status: "success",
              metadata: {},
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
      onSuccess={onSuccess}
      detailed
    />,
    { mocks },
  )

  await waitFor(() => expect(onSuccess).toHaveBeenCalled())
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
      onFail={onFail}
    />,
    { mocks },
  )

  await waitFor(() =>
    expect(onFail).toHaveBeenCalledWith({
      connection: { id: "1", validated: false },
      id: "1",
      metadata: { error: "Run Error", message: "Error Message" },
      status: "error",
    }),
  )
})

test("error result no connection", async () => {
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
                error: "No connection",
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
      onFail={onFail}
    />,
    { mocks },
  )

  await waitFor(() =>
    expect(onFail).toHaveBeenCalledWith({
      connection: { id: "1", validated: false },
      id: "1",
      metadata: { error: "No connection", message: "Error Message" },
      status: "error",
    }),
  )
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
      onFail={onFail}
    />,
    { mocks },
  )

  await waitFor(() =>
    expect(onFail).toHaveBeenCalledWith({
      connection: { id: "1", validated: false },
      id: "1",
      metadata: { error: "Unknown", message: "Error Message" },
      status: "error",
    }),
  )
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
    />,
    { mocks },
  )

  await screen.findByText("Error!")
})
