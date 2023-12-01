import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import SearchParamsTest from "testing/SearchParamsTest"
import ScheduleTab, { GET_CONNECTION } from "./ScheduleTab"

test("submit", async () => {
  const user = userEvent.setup()

  render(<ScheduleTab workspaceId="1" connectionId="1" />, {
    withRouter: true,
    routes: ["/:organisationName/:workspaceName/connections/:connectionId"],
  })

  await screen.findByText(/Schedule type/i)

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /finish/i })),
  )

  await screen.findByText("New Page")
})

test("back", async () => {
  const user = userEvent.setup()

  const onSearchParams = jest.fn()

  render(
    <>
      <ScheduleTab workspaceId="1" connectionId="1" />
      <SearchParamsTest onSearchParams={onSearchParams} />
    </>,
    {
      withRouter: true,
      route: "/default/demo/connections/create?step=schedule&connectionId=1",
      path: "/:organisationName/:workspaceName/connections/create",
    },
  )

  await screen.findByText(/Schedule type/i)

  await act(async () => await user.click(screen.getByTestId("ChevronLeftIcon")))

  await waitFor(async () => {
    expect(onSearchParams).toHaveBeenCalledWith(
      new URLSearchParams("connectionId=1"),
    )
  })
})

test("error", async () => {
  const mocks = [
    {
      request: {
        query: GET_CONNECTION,
        variables: {
          workspaceId: "1",
          connectionId: "1",
        },
      },
      result: {
        errors: [new GraphQLError("Error!")],
      },
    },
  ]

  render(<ScheduleTab workspaceId="1" connectionId="1" />, {
    withRouter: true,
    mocks,
  })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})

test("not found", async () => {
  const mocks = [
    {
      request: {
        query: GET_CONNECTION,
        variables: {
          workspaceId: "1",
          connectionId: "1",
        },
      },
      result: {
        data: {
          workspace: {
            id: "1",
            connection: null,
          },
        },
      },
    },
  ]

  render(<ScheduleTab workspaceId="1" connectionId="1" />, {
    withRouter: true,
    mocks,
  })

  await waitFor(() => {
    expect(screen.getByText("Page not found")).toBeInTheDocument()
  })
})
