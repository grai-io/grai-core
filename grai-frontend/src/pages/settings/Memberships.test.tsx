import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import profileMock from "testing/profileMock"
import { DELETE_MEMBERSHIP } from "components/settings/memberships/MembershipDelete"
import Memberships, { GET_MEMBERSHIPS } from "./Memberships"

test("renders", async () => {
  render(<Memberships />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByText("Memberships")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getAllByText("Hello World")).toBeTruthy()
  })
})

test("error", async () => {
  const mocks = [
    profileMock,
    {
      request: {
        query: GET_MEMBERSHIPS,
        variables: {
          organisationName: "",
          workspaceName: "",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<Memberships />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("empty", async () => {
  const mocks = [
    profileMock,
    {
      request: {
        query: GET_MEMBERSHIPS,
        variables: {
          organisationName: "",
          workspaceName: "",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            memberships: [],
          },
        },
      },
    },
  ]

  render(<Memberships />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Memberships")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getByText("No memberships found")).toBeInTheDocument()
  })
})

test("no workspace", async () => {
  const mocks = [
    profileMock,
    {
      request: {
        query: GET_MEMBERSHIPS,
        variables: {
          organisationName: "",
          workspaceName: "",
        },
      },
      result: {
        data: {
          workspace: null,
        },
      },
    },
  ]

  render(<Memberships />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(
      screen.getByText("Sorry something has gone wrong")
    ).toBeInTheDocument()
  })
})

test("renders and delete", async () => {
  const user = userEvent.setup()

  const mocks = [
    profileMock,
    {
      request: {
        query: GET_MEMBERSHIPS,
        variables: {
          organisationName: "",
          workspaceName: "",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            memberships: [
              {
                id: "1",
                role: "admin",
                user: {
                  id: "2",
                  username: "test@example.com",
                  first_name: "first",
                  last_name: "last",
                },
                is_active: true,
                created_at: "2023-02-24T09:18:48.259220+00:00",
              },
            ],
          },
        },
      },
    },
    {
      request: {
        query: DELETE_MEMBERSHIP,
        variables: {
          id: "1",
        },
      },
      result: {
        data: {
          deleteMembership: {
            id: "1",
          },
        },
      },
    },
  ]

  render(<Memberships />, {
    mocks,
    withRouter: true,
  })

  // console.log(JSON.stringify(cache.extract()))

  await waitFor(() => {
    expect(screen.getByText("Memberships")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(screen.getAllByText("test@example.com")).toBeTruthy()
  })

  await act(async () => await user.click(screen.getByTestId("MoreHorizIcon")))

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i }))
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /delete/i }))
  )

  // await waitFor(() => {
  //   expect(screen.queryAllByText("test@example.com")).toBeFalsy()
  // })
})
