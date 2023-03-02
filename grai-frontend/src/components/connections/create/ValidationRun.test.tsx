import React from "react"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import ValidationRun, { GET_RUN } from "./ValidationRun"

const opts = {
  activeStep: 0,
  setActiveStep: function (activeStep: number): void {
    throw new Error("Function not implemented.")
  },
  forwardStep: function (): void {
    throw new Error("Function not implemented.")
  },
  backStep: function (): void {
    throw new Error("Function not implemented.")
  },
}

const run = {
  id: "1",
}

test("renders queued", async () => {
  render(
    <ValidationRun
      workspaceId="1"
      opts={opts}
      connector={{ id: "1", name: "Test Connector", metadata: null }}
      run={run}
    />,
    {
      withRouter: true,
    }
  )

  await waitFor(async () => {
    expect(screen.getByText("Running")).toBeInTheDocument()
  })
})

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
            },
          },
        },
      },
    },
  ]

  render(
    <ValidationRun
      workspaceId="1"
      opts={opts}
      connector={{ id: "1", name: "Test Connector", metadata: null }}
      run={run}
    />,
    {
      mocks,
      withRouter: true,
    }
  )

  await waitFor(async () => {
    expect(screen.getByText("SUCCESS")).toBeInTheDocument()
  })
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
    <ValidationRun
      workspaceId="1"
      opts={opts}
      connector={{ id: "1", name: "Test Connector", metadata: null }}
      run={run}
    />,
    {
      mocks,
      withRouter: true,
    }
  )

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
