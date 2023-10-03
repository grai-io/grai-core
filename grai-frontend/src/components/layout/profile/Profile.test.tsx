import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import Profile, { GET_PROFILE } from "./Profile"

test("renders", async () => {
  render(<Profile expand />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Hello World Hello World")).toBeTruthy()
  })
})

test("renders collapsed", async () => {
  render(<Profile expand={false} />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("HH")).toBeTruthy()
  })
})

test("renders no name", async () => {
  const mocks = [
    {
      request: {
        query: GET_PROFILE,
      },
      result: {
        data: {
          profile: {
            id: "1",
            username: "test",
            first_name: null,
            last_name: null,
          },
        },
      },
    },
  ]

  render(<Profile expand />, {
    withRouter: true,
    mocks,
  })

  await waitFor(() => {
    expect(screen.getByText("Profile")).toBeTruthy()
  })
})

test("renders no profile", async () => {
  const mocks = [
    {
      request: {
        query: GET_PROFILE,
      },
      result: {
        data: {
          profile: null,
        },
      },
    },
  ]

  render(<Profile expand />, {
    withRouter: true,
    mocks,
  })

  await waitFor(() => {
    expect(screen.queryByText("Profile")).not.toBeInTheDocument()
  })
})

test("logout", async () => {
  render(<Profile expand />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Hello World Hello World")).toBeTruthy()
  })

  await act(
    async () =>
      await userEvent.click(screen.getByText("Hello World Hello World")),
  )

  await waitFor(() => {
    expect(screen.getByText("Logout")).toBeInTheDocument()
  })

  await act(async () => await userEvent.click(screen.getByText("Logout")))
})

test("renders error", async () => {
  const mocks = [
    {
      request: {
        query: GET_PROFILE,
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<Profile expand />, {
    withRouter: true,
    mocks,
  })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
