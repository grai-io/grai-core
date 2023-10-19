import React from "react"
import { userEvent } from "@testing-library/user-event"
import { act, render, screen } from "testing"
import AppDrawerCollapse from "./AppDrawerCollapse"

const setExpand = jest.fn()

test("renders", async () => {
  render(
    <AppDrawerCollapse expand={false} setExpand={setExpand} hover={false} />,
  )

  // expect(screen.queryByTestId("RightIcon")).not.toBeInTheDocument()
  expect(screen.queryByTestId("LeftIcon")).not.toBeInTheDocument()
})

test("expand", async () => {
  const user = userEvent.setup()

  render(<AppDrawerCollapse expand={false} setExpand={setExpand} hover />)

  expect(screen.getByTestId("RightIcon")).toBeInTheDocument()
  expect(screen.queryByTestId("LeftIcon")).not.toBeInTheDocument()

  await act(async () => {
    await user.click(screen.getByTestId("RightIcon"))
  })

  expect(setExpand).toHaveBeenCalledWith(true)
})

test("collapse", async () => {
  const user = userEvent.setup()

  render(<AppDrawerCollapse expand setExpand={setExpand} hover />)

  expect(screen.queryByTestId("RightIcon")).not.toBeInTheDocument()
  expect(screen.getByTestId("LeftIcon")).toBeInTheDocument()

  await act(async () => {
    await user.click(screen.getByTestId("LeftIcon"))
  })

  expect(setExpand).toHaveBeenCalledWith(false)
})
