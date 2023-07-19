import React from "react"
import { Table, TableBody, TableHead, TableRow } from "@mui/material"
import { useNavigate } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"
import ConnectionMenu from "components/connections/ConnectionMenu"
import ConnectorIcon from "components/connectors/ConnectorIcon"
import RunStatus from "components/runs/RunStatus"
import TableCell from "components/tables/TableCell"

interface Connector {
  id: string
  name: string
  icon: string | null
}

interface Run {
  id: string
  status: string
}

export interface Connection {
  id: string
  name: string
  connector: Connector
  last_run: Run | null
}

type SourceConnectionsTableProps = {
  connections: Connection[]
  workspaceId: string
}

const SourceConnectionsTable: React.FC<SourceConnectionsTableProps> = ({
  connections,
  workspaceId,
}) => {
  const { routePrefix } = useWorkspace()
  const navigate = useNavigate()

  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell colSpan={2}>Name</TableCell>
          <TableCell>Status</TableCell>
          <TableCell sx={{ width: 0 }} />
        </TableRow>
      </TableHead>
      <TableBody>
        {connections.map(connection => (
          <TableRow
            key={connection.id}
            hover
            onClick={() =>
              navigate(`${routePrefix}/connections/${connection.id}`)
            }
            sx={{ cursor: "pointer" }}
          >
            <TableCell sx={{ p: 0, width: 0 }}>
              <ConnectorIcon connector={connection.connector} noBorder />
            </TableCell>
            <TableCell>{connection.name}</TableCell>
            <TableCell sx={{ p: 0 }}>
              {connection.last_run && <RunStatus run={connection.last_run} />}
            </TableCell>
            <TableCell sx={{ p: 0 }} stopPropagation>
              <ConnectionMenu
                workspaceId={workspaceId}
                connection={connection}
              />
            </TableCell>
          </TableRow>
        ))}
        {connections.length === 0 && (
          <TableRow>
            <TableCell colSpan={99} sx={{ textAlign: "center", py: 10 }}>
              No connections found
            </TableCell>
          </TableRow>
        )}
      </TableBody>
    </Table>
  )
}

export default SourceConnectionsTable
