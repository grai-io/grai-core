import React from "react"
import userEvent from "@testing-library/user-event"
import { GraphQLError } from "graphql"
import { act, fireEvent, render, screen, waitFor, within } from "testing"
import FilterControl, { GET_FILTERS } from "./FilterControl"

test("renders", async () => {
  render(<FilterControl />, {
    withRouter: true,
  })

  expect(screen.getByTestId("FilterAltIcon")).toBeInTheDocument()

  await waitFor(() => {
    expect(screen.queryByRole("progressbar")).not.toBeInTheDocument()
  })
})

test("create", async () => {
  render(<FilterControl />, {
    withRouter: true,
    routes: ["/:organisationName/:workspaceName/filters/create"],
  })

  expect(screen.getByTestId("FilterAltIcon")).toBeInTheDocument()

  await waitFor(() => {
    expect(screen.queryByRole("progressbar")).not.toBeInTheDocument()
  })

  const autocomplete = screen.getByTestId("filter-control")
  autocomplete.focus()
  const input = within(autocomplete).getByRole("combobox")
  // the value here can be any string you want, so you may also consider to
  // wrapper it as a function and pass in inputValue as parameter
  fireEvent.change(input, { target: { value: "a" } })
  fireEvent.keyDown(autocomplete, { key: "ArrowDown" })
  fireEvent.keyDown(autocomplete, { key: "Enter" })

  await waitFor(() => {
    expect(screen.getByText("New Page")).toBeInTheDocument()
  })
})

test("manage", async () => {
  render(<FilterControl />, {
    withRouter: true,
    routes: ["/:organisationName/:workspaceName/filters"],
  })

  expect(screen.getByTestId("FilterAltIcon")).toBeInTheDocument()

  await waitFor(() => {
    expect(screen.queryByRole("progressbar")).not.toBeInTheDocument()
  })

  const autocomplete = screen.getByTestId("filter-control")
  autocomplete.focus()
  const input = within(autocomplete).getByRole("combobox")
  // the value here can be any string you want, so you may also consider to
  // wrapper it as a function and pass in inputValue as parameter
  fireEvent.change(input, { target: { value: "a" } })
  fireEvent.keyDown(autocomplete, { key: "ArrowDown" })
  fireEvent.keyDown(autocomplete, { key: "ArrowDown" })
  fireEvent.keyDown(autocomplete, { key: "Enter" })

  await waitFor(() => {
    expect(screen.getByText("New Page")).toBeInTheDocument()
  })
})

test("select filter", async () => {
  const user = userEvent.setup()

  render(<FilterControl />, {
    withRouter: true,
    routes: ["/:organisationName/:workspaceName/filters"],
  })

  expect(screen.getByTestId("FilterAltIcon")).toBeInTheDocument()

  await waitFor(() => {
    expect(screen.queryByRole("progressbar")).not.toBeInTheDocument()
  })

  const autocomplete = screen.getByTestId("filter-control")
  autocomplete.focus()
  const input = within(autocomplete).getByRole("combobox")
  // the value here can be any string you want, so you may also consider to
  // wrapper it as a function and pass in inputValue as parameter
  fireEvent.change(input, { target: { value: "a" } })
  fireEvent.keyDown(autocomplete, { key: "ArrowDown" })
  fireEvent.keyDown(autocomplete, { key: "ArrowDown" })
  fireEvent.keyDown(autocomplete, { key: "ArrowDown" })
  fireEvent.keyDown(autocomplete, { key: "Enter" })

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})

  await user.click(screen.getByTestId("CloseIcon"))

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})
})

test("empty", async () => {
  const mocks = [
    {
      request: {
        query: GET_FILTERS,
        variables: {
          organisationName: "",
          workspaceName: "",
        },
      },
      result: {
        data: {
          filters: {
            data: [],
          },
        },
      },
    },
  ]

  render(<FilterControl />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.queryByRole("progressbar")).not.toBeInTheDocument()
  })

  const autocomplete = screen.getByTestId("filter-control")
  autocomplete.focus()
  const input = within(autocomplete).getByRole("combobox")
  // the value here can be any string you want, so you may also consider to
  // wrapper it as a function and pass in inputValue as parameter
  fireEvent.change(input, { target: { value: "a" } })
  fireEvent.keyDown(autocomplete, { key: "ArrowDown" })
})

test("error", async () => {
  const mocks = [
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

  render(<FilterControl />, { mocks, withRouter: true })

  await waitFor(() => {
    expect(screen.getByText("Error!")).toBeInTheDocument()
  })
})
