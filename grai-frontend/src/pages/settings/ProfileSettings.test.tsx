import { GraphQLError } from "graphql"
import React from "react"
import { renderWithMocks, renderWithRouter, screen, waitFor } from "testing"
import ProfileSettings, { GET_PROFILE } from "./ProfileSettings"

test("renders", async () => {
  renderWithRouter(<ProfileSettings />)

  await waitFor(() => {
    expect(screen.getByText("Profile Settings")).toBeTruthy()
  })
})

test("error", async () => {
  const mock = {
    request: {
      query: GET_PROFILE,
    },
    result: {
      errors: [new GraphQLError("Error!")],
    },
  }

  renderWithMocks(<ProfileSettings />, [mock])

  await waitFor(() => {
    expect(screen.getAllByText("Error!")).toBeTruthy()
  })
})

test("not found", async () => {
  const mock = {
    request: {
      query: GET_PROFILE,
    },
    result: {
      data: {
        profile: null,
      },
    },
  }

  renderWithMocks(<ProfileSettings />, [mock])

  await waitFor(() => {
    expect(screen.getAllByText("Page not found")).toBeTruthy()
  })
})
