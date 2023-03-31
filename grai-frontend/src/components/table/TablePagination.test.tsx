import React from "react"
import { Table, TableFooter } from "@mui/material"
import userEvent from "@testing-library/user-event"
import { render, screen } from "testing"
import TablePagination from "./TablePagination"

test("renders", async () => {
  render(
    <Table>
      <TableFooter>
        <TablePagination
          count={10}
          rowsPerPage={15}
          page={0}
          onPageChange={() => {}}
        />
      </TableFooter>
    </Table>
  )
})

test("renders one", async () => {
  render(
    <Table>
      <TableFooter>
        <TablePagination
          count={1}
          rowsPerPage={15}
          page={0}
          onPageChange={() => {}}
        />
      </TableFooter>
    </Table>
  )
})

test("next", async () => {
  const user = userEvent.setup()

  render(
    <Table>
      <TableFooter>
        <TablePagination
          count={20}
          rowsPerPage={15}
          page={0}
          onPageChange={() => {}}
        />
      </TableFooter>
    </Table>
  )

  await user.click(screen.getByRole("button", { name: /next/i }))
})

test("previous", async () => {
  const user = userEvent.setup()

  render(
    <Table>
      <TableFooter>
        <TablePagination
          count={20}
          rowsPerPage={15}
          page={1}
          onPageChange={() => {}}
        />
      </TableFooter>
    </Table>
  )

  await user.click(screen.getByRole("button", { name: /previous/i }))
})
