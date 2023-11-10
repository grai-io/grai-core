import { Table, TableFooter } from "@mui/material"
import userEvent from "@testing-library/user-event"
import { act, render, screen } from "testing"
import TablePagination from "./TablePagination"

const onPageChange = jest.fn()

test("renders", async () => {
  render(
    <Table>
      <TableFooter>
        <TablePagination
          count={10}
          rowsPerPage={15}
          page={0}
          onPageChange={onPageChange}
        />
      </TableFooter>
    </Table>,
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
          onPageChange={onPageChange}
        />
      </TableFooter>
    </Table>,
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
          onPageChange={onPageChange}
        />
      </TableFooter>
    </Table>,
  )

  await act(
    async () => await user.click(screen.getByRole("button", { name: /next/i })),
  )

  expect(onPageChange).toHaveBeenCalledWith(1)
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
          onPageChange={onPageChange}
        />
      </TableFooter>
    </Table>,
  )

  await act(
    async () =>
      await user.click(screen.getByRole("button", { name: /previous/i })),
  )

  expect(onPageChange).toHaveBeenCalledWith(0)
})
