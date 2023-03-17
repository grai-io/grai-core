import React from "react"
import { Card, Table, TableBody } from "@mui/material"
import NodeDetailRow from "components/layout/NodeDetailRow"
import ConnectionSchedule, {
  Connection as BaseConnection,
} from "./schedule/ConnectionSchedule"

interface Run {
  id: string
  status: string
}

interface Connector {
  id: string
  name: string
  metadata: any
}

interface Connection extends BaseConnection {
  id: string
  name: string
  namespace: string
  connector: Connector
  last_run: Run | null
  last_successful_run: Run | null
  metadata: any
}

type ConnectionDetailProps = {
  connection: Connection
}

const ConnectionDetail: React.FC<ConnectionDetailProps> = ({ connection }) => (
  <Card variant="outlined" sx={{ borderRadius: 0, borderBottom: 0 }}>
    <Table>
      <TableBody>
        <NodeDetailRow label="id" value={connection.id} />
        <NodeDetailRow label="Integration" value={connection.connector.name} />
        <ConnectionSchedule connection={connection} />
      </TableBody>
    </Table>
  </Card>
)

export default ConnectionDetail
