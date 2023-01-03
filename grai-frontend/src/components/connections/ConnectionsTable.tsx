import {
  Table,
  TableBody,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material"
import React from "react"
import { useNavigate } from "react-router-dom"
import Loading from "components/layout/Loading"
import TableCell from "components/tables/TableCell"
import ConnectionsMenu from "./ConnectionsMenu"

interface Run {
  id: string
  status: string
}

interface Connector {
  id: string
  name: string
}

interface Connection {
  id: string
  namespace: string
  name: string
  connector: Connector
  is_active: boolean
  last_run: Run | null
}

type ConnectionsTableProps = {
  connections: Connection[]
  loading?: boolean
}

const ConnectionsTable: React.FC<ConnectionsTableProps> = ({
  connections,
  loading,
}) => {
  const navigate = useNavigate()

  return (
    <Table>
      <TableHead>
        <TableRow sx={{ backgroundColor: theme => theme.palette.grey[100] }}>
          <TableCell>Name</TableCell>
          <TableCell>Namespace</TableCell>
          <TableCell>Connector</TableCell>
          <TableCell>Active</TableCell>
          <TableCell sx={{ width: 0 }} />
        </TableRow>
      </TableHead>
      <TableBody>
        {connections.map(connection => (
          <TableRow
            key={connection.id}
            hover
            sx={{ cursor: "pointer" }}
            onClick={() => navigate(connection.id)}
          >
            <TableCell>{connection.name}</TableCell>
            <TableCell>{connection.namespace}</TableCell>
            <TableCell>{connection.connector.name}</TableCell>
            <TableCell>{connection.is_active ? "Yes" : "No"}</TableCell>
            <TableCell sx={{ py: 0, px: 1 }} stopPropagation>
              <ConnectionsMenu connection={connection} />
            </TableCell>
          </TableRow>
        ))}
        {!loading && connections.length === 0 && (
          <TableRow>
            <TableCell colSpan={99} sx={{ textAlign: "center", py: 10 }}>
              <Typography>No connections found</Typography>
            </TableCell>
          </TableRow>
        )}
        {loading && (
          <TableRow>
            <TableCell colSpan={99}>
              <Loading />
            </TableCell>
          </TableRow>
        )}
      </TableBody>
    </Table>
  )
}

export default ConnectionsTable
