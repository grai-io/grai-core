import React from "react"
import userEvent from "@testing-library/user-event"
import { act, render, screen } from "testing"
import LoadMoreControl from "./LoadMoreControl"

test("renders", async () => {
  render(
    <LoadMoreControl
      options={{
        count: 10,
        total: 20,
        onLoadMore: () => {},
      }}
    />
  )

  expect(screen.getByRole("button", { name: /Load more/i })).toBeInTheDocument()
})

test("load more", async () => {
  const user = userEvent.setup()

  render(
    <LoadMoreControl
      options={{
        count: 10,
        total: 20,
        onLoadMore: () => {},
      }}
    />
  )

  expect(screen.getByRole("button", { name: /Load more/i })).toBeInTheDocument()

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /Load more/i }))
  )
})
