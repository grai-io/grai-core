import { Table, TableBody } from "@mui/material"
import userEvent from "@testing-library/user-event"
import React from "react"
import { render, screen } from "testing"
import ConnectionProperties from "./ConnectionProperties"

const connection = {
  id: "1",
  name: "test connection",
  namespace: "default",
  connector: {
    id: "1",
    name: "test connector",
    metadata: {
      fields: [
        {
          name: "field 1",
        },
        {
          name: "field 2",
          secret: true,
        },
      ],
    },
  },
  metadata: {},
  last_run: null,
}

test("renders", async () => {
  render(
    <Table>
      <TableBody>
        <ConnectionProperties connection={connection} />
      </TableBody>
    </Table>
  )
})

test("edit", async () => {
  const user = userEvent.setup()

  render(
    <Table>
      <TableBody>
        <ConnectionProperties connection={connection} />
      </TableBody>
    </Table>
  )

  await user.click(screen.getByRole("button", { name: /edit/i }))

  await user.click(screen.getByTestId("CloseIcon"))
})
