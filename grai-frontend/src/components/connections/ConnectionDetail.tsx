import { Card, Table, TableBody } from "@mui/material"
import NodeDetailRow from "components/nodes/NodeDetailRow"
import React from "react"
import ConnectionProperties from "./ConnectionProperties"

interface Run {
  id: string
  status: string
}

interface Connector {
  id: string
  name: string
  metadata: any
}

interface Connection {
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
        <NodeDetailRow label="Connector" value={connection.connector.name} />
        <ConnectionProperties connection={connection} />
      </TableBody>
    </Table>
  </Card>
)

export default ConnectionDetail
