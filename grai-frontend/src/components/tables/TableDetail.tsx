import React from "react"
import { Card, Table, TableBody } from "@mui/material"
import valueToString from "helpers/valueToString"
import NodeDetailRow from "components/layout/NodeDetailRow"

interface TableInterface {
  name: string
  namespace: string
  data_source: string
  metadata?: any | null
}

type TableDetailProps = {
  table: TableInterface
}

const TableDetail: React.FC<TableDetailProps> = ({ table }) => (
  <Card variant="outlined" sx={{ borderRadius: 0, borderBottom: 0 }}>
    <Table>
      <TableBody>
        <NodeDetailRow label="Last updated at" />
        <NodeDetailRow label="# of rows" />
        <NodeDetailRow label="# of columns" />
        <NodeDetailRow label="Name" value={table.name} />
        <NodeDetailRow label="Namespace" value={table.namespace} />
        <NodeDetailRow label="Data Source" value={table.data_source} />
        {table.metadata &&
          Object.entries(table.metadata).map(([key, value]) => (
            <NodeDetailRow key={key} label={key} value={valueToString(value)} />
          ))}
      </TableBody>
    </Table>
  </Card>
)

export default TableDetail
