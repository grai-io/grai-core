import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen } from "testing"
import { DELETE_MEMBERSHIP } from "components/settings/memberships/MembershipDelete"
import Memberships, { GET_MEMBERSHIPS } from "./Memberships"

test("renders", async () => {
  render(<Memberships />, {
    withRouter: true,
  })

  await screen.findByText("Memberships")

  await screen.findAllByText("Hello World")
})

test("error", async () => {
  const mocks = [
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

  await screen.findByText("Error!")
})

test("empty", async () => {
  const mocks = [
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
            memberships: { data: [], meta: { total: 0 } },
          },
        },
      },
    },
  ]

  render(<Memberships />, { mocks, withRouter: true })

  await screen.findByText("Memberships")

  await screen.findByText("No memberships found")
})

test("no workspace", async () => {
  const mocks = [
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

  await screen.findByText("Sorry something has gone wrong")
})

test("renders and delete", async () => {
  const user = userEvent.setup()

  const mocks = [
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
            memberships: {
              data: [
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
              meta: { total: 1 },
            },
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

  await screen.findByText("Memberships")

  await screen.findAllByText("test@example.com")

  await act(async () => await user.click(screen.getByTestId("MoreHorizIcon")))

  await act(
    async () =>
      await user.click(screen.getByRole("menuitem", { name: /delete/i })),
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /delete/i })),
  )

  // await waitFor(() =>
  //   expect(screen.queryAllByText("test@example.com")).toBeFalsy()
  // )
})
