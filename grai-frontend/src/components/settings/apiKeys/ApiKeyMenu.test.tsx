import React from "react"
import userEvent from "@testing-library/user-event"
import { act, render, screen } from "testing"
import ApiKeyMenu from "./ApiKeyMenu"

const apiKey = {
  id: "1",
  name: "key 1",
  prefix: "1234a",
  created: "2021-01-21",
  revoked: false,
  expiryDate: null,
  createdBy: {
    id: "1",
    username: "edward",
  },
}

test("renders", async () => {
  const user = userEvent.setup()

  render(<ApiKeyMenu apiKey={apiKey} />)

  await act(async () => await user.click(screen.getByTestId("MoreHorizIcon")))
})
