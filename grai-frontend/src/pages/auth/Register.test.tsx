import React from "react"
import { render, waitFor } from "testing"
import Register from "./Register"

test("renders", async () => {
  render(<Register />, {
    withRouter: true,
  })

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {})
})
