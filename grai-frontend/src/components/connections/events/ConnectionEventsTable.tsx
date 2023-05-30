import React from "react"
import {
  Box,
  Button,
  Table,
  TableBody,
  TableCell,
  TableFooter,
  TableHead,
  TableRow,
} from "@mui/material"
import { DateTime } from "luxon"
import { Link } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"
import ConnectorIcon from "components/connectors/ConnectorIcon"
import TablePagination from "components/table/TablePagination"

interface Connection {
  id: string
  name: string
  connector: {
    name: string
    icon: string | null
  }
}

interface Event {
  id: string
  status: string
  date: string
  connection?: Connection
}

type ConnectionEventsTableProps = {
  events: Event[]
  total: number
  connections?: boolean
}

const ConnectionEventsTable: React.FC<ConnectionEventsTableProps> = ({
  events,
  total,
  connections,
}) => {
  const { routePrefix } = useWorkspace()

  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>id</TableCell>
          <TableCell>Status</TableCell>
          <TableCell>Date</TableCell>
          {connections && <TableCell>Connection</TableCell>}
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
            {connections && event.connection && (
              <TableCell sx={{ py: 0 }}>
                <Box sx={{ display: "flex", alignItems: "center" }}>
                  <ConnectorIcon
                    connector={event.connection.connector}
                    noBorder
                  />
                  <Button
                    sx={{ ml: 1 }}
                    component={Link}
                    to={`${routePrefix}/connections/${event.connection.id}`}
                  >
                    {event.connection.name}
                  </Button>
                </Box>
              </TableCell>
            )}
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
}

export default ConnectionEventsTable
