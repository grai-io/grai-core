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
import { DateTime } from "luxon"

interface Event {
  id: string
  status: string
  date: string
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
        <TableCell>Date</TableCell>
      </TableRow>
    </TableHead>
    <TableBody>
      {events.map(event => (
        <TableRow key={event.id}>
          <TableCell>{event.id}</TableCell>
          <TableCell>{event.status}</TableCell>
          <TableCell>
            {DateTime.fromISO(event.date).toLocaleString(
              DateTime.DATETIME_FULL
            )}
          </TableCell>
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
