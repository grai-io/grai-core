import React from "react"
import userEvent from "@testing-library/user-event"
import { render, screen } from "testing"
import StepsControl from "./StepsControl"

test("renders", async () => {
  let value = 1
  const setValue = (input: number) => (value = input)

  render(
    <StepsControl
      options={{
        value,
        setValue,
      }}
    />
  )

  expect(screen.getByTestId("AddIcon")).toBeInTheDocument()
  expect(screen.getByTestId("RemoveIcon")).toBeInTheDocument()
})

test("plus", async () => {
  let value = 1
  const setValue = (input: number) => (value = input)

  const user = userEvent.setup()

  render(
    <StepsControl
      options={{
        value,
        setValue,
      }}
    />
  )

  expect(value).toEqual(1)

  expect(screen.getByTestId("AddIcon")).toBeInTheDocument()
  expect(screen.getByTestId("RemoveIcon")).toBeInTheDocument()

  await user.click(screen.getByTestId("AddIcon"))

  expect(value).toEqual(2)
})

test("minus", async () => {
  let value = 2
  const setValue = (input: number) => (value = input)

  const user = userEvent.setup()

  render(
    <StepsControl
      options={{
        value,
        setValue,
      }}
    />
  )

  expect(value).toEqual(2)

  expect(screen.getByTestId("AddIcon")).toBeInTheDocument()
  expect(screen.getByTestId("RemoveIcon")).toBeInTheDocument()

  await user.click(screen.getByTestId("RemoveIcon"))

  expect(value).toEqual(1)
})

test("change", async () => {
  let value = 1
  const setValue = (input: number) => (value = input)

  const user = userEvent.setup()

  render(
    <StepsControl
      options={{
        value,
        setValue,
      }}
    />
  )

  expect(value).toEqual(1)

  await user.type(screen.getByRole("textbox"), "1")

  expect(value).toEqual(11)
})
