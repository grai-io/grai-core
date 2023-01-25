import { Card, Table, TableBody } from "@mui/material"
import React from "react"
import NodeDetailRow from "./NodeDetailRow"

interface Node {
  name: string
  namespace: string
  data_source: string
  metadata: any
}

type NodeDetailProps = {
  node: Node
}

const valueToString = (value: any): string => {
  switch (typeof value) {
    case "string":
      return value
    case "boolean":
      return value ? "yes" : "no"
  }

  return JSON.stringify(value)
}

const NodeDetail: React.FC<NodeDetailProps> = ({ node }) => (
  <Card variant="outlined" sx={{ borderRadius: 0, borderBottom: 0 }}>
    <Table>
      <TableBody>
        <NodeDetailRow label="Last updated at" />
        <NodeDetailRow label="# of rows" />
        <NodeDetailRow label="# of columns" />
        <NodeDetailRow label="Name" value={node.name} />
        <NodeDetailRow label="Namespace" value={node.namespace} />
        <NodeDetailRow label="Data Source" value={node.data_source} />
        {Object.entries(node.metadata).map(([key, value]) => (
          <NodeDetailRow key={key} label={key} value={valueToString(value)} />
        ))}
      </TableBody>
    </Table>
  </Card>
)

export default NodeDetail
