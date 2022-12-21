import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import React from "react"
import {
  render,
  renderWithMocks,
  renderWithRouter,
  screen,
  waitFor,
} from "testing"
import ProfileForm, { UPDATE_PROFILE } from "./ProfileForm"

const profile = {
  username: "test@example.com",
  firstName: "test",
  lastName: "example",
}

test("renders", async () => {
  render(<ProfileForm profile={profile} />)

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

  render(<ProfileForm profile={profile} />)

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

  await user.type(screen.getByRole("textbox", { name: /First Name/i }), "a")
  await user.type(screen.getByRole("textbox", { name: /Last Name/i }), "b")

  await user.click(screen.getByRole("button", { name: /save/i }))
})

test("error", async () => {
  const user = userEvent.setup()

  const mock = {
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
  }

  renderWithMocks(<ProfileForm profile={profile} />, [mock])

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

  await user.type(screen.getByRole("textbox", { name: /First Name/i }), "a")
  await user.type(screen.getByRole("textbox", { name: /Last Name/i }), "b")

  await user.click(screen.getByRole("button", { name: /save/i }))

  await waitFor(() => {
    expect(screen.getAllByText("Error!")).toBeTruthy()
  })
})
