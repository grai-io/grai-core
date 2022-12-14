import {
  Checkbox,
  Table,
  TableBody,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material"
import React from "react"
import { useNavigate } from "react-router-dom"
import Loading from "../layout/Loading"
import TableCell from "../tables/TableCell"
import ConnectionsMenu from "./ConnectionsMenu"

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
}) => {
  const navigate = useNavigate()

  return (
    <Table size="small">
      <TableHead>
        <TableRow>
          <TableCell sx={{ p: 0, width: 0 }}>
            <Checkbox size="small" />
          </TableCell>
          <TableCell>id</TableCell>
          <TableCell>Namespace</TableCell>
          <TableCell>Name</TableCell>
          <TableCell>Connector</TableCell>
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
            <TableCell sx={{ p: 0 }} stopPropagation>
              <Checkbox size="small" />
            </TableCell>
            <TableCell>{connection.id}</TableCell>
            <TableCell>{connection.namespace}</TableCell>
            <TableCell>{connection.name}</TableCell>
            <TableCell>{connection.connector.name}</TableCell>
            <TableCell sx={{ py: 0, px: 1 }} stopPropagation>
              <ConnectionsMenu connection={connection} />
            </TableCell>
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
              <Loading />
            </TableCell>
          </TableRow>
        )}
      </TableBody>
    </Table>
  )
}

export default ConnectionsTable
