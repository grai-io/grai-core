import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import ProfileForm, { UPDATE_PROFILE } from "./ProfileForm"

const profile = {
  username: "test@example.com",
  first_name: "test",
  last_name: "example",
}

test("renders", async () => {
  render(<ProfileForm profile={profile} />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(
      screen.getByRole("textbox", {
        name: /Email/i,
      })
    ).toHaveValue("test@example.com")
  })

  await waitFor(() => {
    expect(
      screen.getByRole("textbox", {
        name: /First Name/i,
      })
    ).toHaveValue("test")
  })

  await waitFor(() => {
    expect(
      screen.getByRole("textbox", {
        name: /Last Name/i,
      })
    ).toHaveValue("example")
  })
})

test("submit", async () => {
  const user = userEvent.setup()

  render(<ProfileForm profile={profile} />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(
      screen.getByRole("textbox", {
        name: /Email/i,
      })
    ).toHaveValue("test@example.com")
  })

  await waitFor(() => {
    expect(
      screen.getByRole("textbox", {
        name: /First Name/i,
      })
    ).toHaveValue("test")
  })

  await waitFor(() => {
    expect(
      screen.getByRole("textbox", {
        name: /Last Name/i,
      })
    ).toHaveValue("example")
  })

  await act(
    async () =>
      await user.type(screen.getByRole("textbox", { name: /First Name/i }), "a")
  )
  await act(
    async () =>
      await user.type(screen.getByRole("textbox", { name: /Last Name/i }), "b")
  )

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i }))
  )
})

test("error", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: UPDATE_PROFILE,
        variables: {
          first_name: "testa",
          last_name: "exampleb",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<ProfileForm profile={profile} />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(
      screen.getByRole("textbox", {
        name: /Email/i,
      })
    ).toHaveValue("test@example.com")
  })

  await waitFor(() => {
    expect(
      screen.getByRole("textbox", {
        name: /First Name/i,
      })
    ).toHaveValue("test")
  })

  await waitFor(() => {
    expect(
      screen.getByRole("textbox", {
        name: /Last Name/i,
      })
    ).toHaveValue("example")
  })

  await act(
    async () =>
      await user.type(screen.getByRole("textbox", { name: /First Name/i }), "a")
  )
  await act(
    async () =>
      await user.type(screen.getByRole("textbox", { name: /Last Name/i }), "b")
  )

  await act(
    async () => await user.click(screen.getByRole("button", { name: /save/i }))
  )

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
