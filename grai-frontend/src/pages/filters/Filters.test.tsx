import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, render, screen, waitFor } from "testing"
import profileMock from "testing/profileMock"
// import { DELETE_FILTER } from "components/filters/FilterDelete"
import Filters, { GET_FILTERS } from "./Filters"

test("renders", async () => {
  render(<Filters />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: /Filters/i })).toBeTruthy()
  })

  await waitFor(() => {
    expect(screen.getAllByText("Hello World")).toBeTruthy()
  })
})

test("refresh", async () => {
  const user = userEvent.setup()

  render(<Filters />, {
    withRouter: true,
  })

  await waitFor(() => {
    expect(screen.getByRole("heading", { name: /Filters/i })).toBeTruthy()
  })

  await act(async () => await user.click(screen.getByTestId("filter-refresh")))

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})
})

// const filterMock = {
//   request: {
//     query: GET_FILTERS,
//     variables: {
//       organisationName: "",
//       workspaceName: "",
//     },
//   },
//   result: {
//     data: {
//       workspace: {
//         id: "1",
//         filters: {
//           data: [
//             {
//               id: "1",
//               namespace: "default",
//               name: "Filter 1",
//               is_active: true,
//               connector: {
//                 id: "1",
//                 name: "Connector 1",
//               },
//               runs: { data: [] },
//               last_run: null,
//               last_successful_run: null,
//             },
//           ],
//           meta: {
//             total: 1,
//           },
//         },
//       },
//     },
//   },
// }

// test("delete", async () => {
//   const user = userEvent.setup()

//   const mocks = [
//     profileMock,
//     filterMock,
//     {
//       request: {
//         query: DELETE_FILTER,
//         variables: {
//           id: "1",
//         },
//       },
//       result: {
//         data: {
//           deleteFilter: {
//             id: "1",
//           },
//         },
//       },
//     },
//   ]

//   render(<Filters />, {
//     withRouter: true,
//     mocks,
//   })

//   await waitFor(() => {
//     expect(screen.getByRole("heading", { name: /Filters/i })).toBeTruthy()
//   })

//   await waitFor(() => {
//     expect(screen.getAllByText("Filter 1")).toBeTruthy()
//   })

//   await act(async () => {
//     await user.click(screen.getByTestId("MoreHorizIcon"))
//   })

//   await act(
//     async () =>
//       await user.click(screen.getByRole("menuitem", { name: /delete/i }))
//   )

//   await act(
//     async () =>
//       await user.click(screen.getByRole("button", { name: /delete/i }))
//   )
// })

// test("cancel delete", async () => {
//   const user = userEvent.setup()

//   const mocks = [
//     profileMock,
//     filterMock,
//     {
//       request: {
//         query: DELETE_FILTER,
//         variables: {
//           id: "1",
//         },
//       },
//       result: {
//         data: {
//           deleteFilter: {
//             id: "1",
//           },
//         },
//       },
//     },
//   ]

//   render(<Filters />, {
//     withRouter: true,
//     mocks,
//   })

//   await waitFor(() => {
//     expect(screen.getByRole("heading", { name: /Filters/i })).toBeTruthy()
//   })

//   await waitFor(() => {
//     expect(screen.getAllByText("Filter 1")).toBeTruthy()
//   })

//   await act(async () => {
//     await user.click(screen.getByTestId("MoreHorizIcon"))
//   })

//   await act(
//     async () =>
//       await user.click(screen.getByRole("menuitem", { name: /delete/i }))
//   )

//   await act(
//     async () =>
//       await user.click(screen.getByRole("button", { name: /cancel/i }))
//   )
// })

test("error", async () => {
  const mocks = [
    profileMock,
    {
      request: {
        query: GET_FILTERS,
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

  render(<Filters />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})