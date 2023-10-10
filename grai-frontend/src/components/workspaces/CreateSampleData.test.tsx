import React from "react"
import { GraphQLError } from "graphql"
import { render, screen, waitFor } from "testing"
import CreateSampleData, {
  LOAD_WORKSPACE_SAMPLE_DATA,
} from "./CreateSampleData"

const workspace = {
  id: "1",
  name: "production",
  organisation: {
    id: "1",
    name: "TestOrganisation",
  },
}

test("error", async () => {
  const mocks = [
    {
      request: {
        query: LOAD_WORKSPACE_SAMPLE_DATA,
        variables: {
          id: "1",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<CreateSampleData workspace={workspace} />, {
    mocks,
    withRouter: true,
  })

  await waitFor(() =>
    expect(screen.getByText(/Your workspace will be ready very soon/i)),
  )

  await waitFor(() => expect(screen.getByText(/Error!/i)))
})
