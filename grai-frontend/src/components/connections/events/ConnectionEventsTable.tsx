import React from "react"
import {
  Table,
  TableBody,
  TableCell,
  TableFooter,
  TableHead,
  TableRow,
} from "@mui/material"
import TablePagination from "components/table/TablePagination"

interface Event {
  id: string
  status: string
  created_at: string
}

type ConnectionEventsTableProps = {
  events: Event[]
  total: number
}

const ConnectionEventsTable: React.FC<ConnectionEventsTableProps> = ({
  events,
  total,
}) => (
  <Table>
    <TableHead>
      <TableRow>
        <TableCell>id</TableCell>
        <TableCell>Status</TableCell>
        <TableCell>Created At</TableCell>
      </TableRow>
    </TableHead>
    <TableBody>
      {events.map(event => (
        <TableRow key={event.id}>
          <TableCell>{event.id}</TableCell>
          <TableCell>{event.status}</TableCell>
          <TableCell>{event.created_at}</TableCell>
        </TableRow>
      ))}
    </TableBody>
    <TableFooter>
      <TablePagination
        count={total}
        rowsPerPage={1000}
        page={0}
        type="events"
      />
    </TableFooter>
  </Table>
)

export default ConnectionEventsTable
