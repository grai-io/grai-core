import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import OrganisationForm, { CREATE_WORKSPACE } from "./OrganisationForm"

test("renders", async () => {
  const user = userEvent.setup()

  render(<OrganisationForm />, {
    routes: ["/Hello World/Hello World"],
  })

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: /name/i }),
        "TestOrganisation"
      )
  )

  await act(
    async () => await user.click(screen.getByRole("button", { name: /next/i }))
  )

  await waitFor(() => {
    expect(screen.getByText("New Page")).toBeInTheDocument()
  })
})

test("error", async () => {
  const user = userEvent.setup()

  const mocks = [
    {
      request: {
        query: CREATE_WORKSPACE,
        variables: {
          name: "production",
          organisationName: "TestOrganisation",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<OrganisationForm />, {
    withRouter: true,
    mocks,
  })

  await act(
    async () =>
      await user.type(
        screen.getByRole("textbox", { name: /name/i }),
        "TestOrganisation"
      )
  )

  await act(
    async () => await user.click(screen.getByRole("button", { name: /next/i }))
  )

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
