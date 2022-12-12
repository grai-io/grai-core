import {
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material"
import React from "react"

interface Connector {
  id: string
  name: string
}

interface Connection {
  id: string
  namespace: string
  name: string
  connector: Connector
}

type ConnectionsTableProps = {
  connections: Connection[]
  loading?: boolean
}

const ConnectionsTable: React.FC<ConnectionsTableProps> = ({
  connections,
  loading,
}) => (
  <Table size="small">
    <TableHead>
      <TableRow>
        <TableCell>id</TableCell>
        <TableCell>Namespace</TableCell>
        <TableCell>Name</TableCell>
        <TableCell>Connector</TableCell>
        <TableCell />
      </TableRow>
    </TableHead>
    <TableBody>
      {connections.map(connection => (
        <TableRow key={connection.id}>
          <TableCell>{connection.id}</TableCell>
          <TableCell>{connection.namespace}</TableCell>
          <TableCell>{connection.name}</TableCell>
          <TableCell>{connection.connector.name}</TableCell>
          <TableCell />
        </TableRow>
      ))}
      {!loading && connections.length === 0 && (
        <TableRow>
          <TableCell colSpan={99} sx={{ textAlign: "center", py: 5 }}>
            <Typography>No Connections</Typography>
          </TableCell>
        </TableRow>
      )}
      {loading && (
        <TableRow>
          <TableCell colSpan={99}>
            <CircularProgress />
          </TableCell>
        </TableRow>
      )}
    </TableBody>
  </Table>
)

export default ConnectionsTable
