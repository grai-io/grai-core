import { Card, Table, TableBody } from "@mui/material"
import React from "react"
import NodeDetailRow from "./NodeDetailRow"

interface Node {
  name: string
  metadata: any
}

type NodeDetailProps = {
  node: Node
}

const NodeDetail: React.FC<NodeDetailProps> = ({ node }) => (
  <Card variant="outlined" sx={{ borderRadius: 0, borderBottom: 0 }}>
    <Table>
      <TableBody>
        <NodeDetailRow label="Last updated at" />
        <NodeDetailRow label="# of rows" />
        <NodeDetailRow label="# of columns" />
        <NodeDetailRow label="Name" value={node.name} />
        {Object.entries(node.metadata).map(([key, value]) => (
          <NodeDetailRow
            key={key}
            label={key}
            value={typeof value === "string" ? value : value ? "yes" : "no"}
          />
        ))}
      </TableBody>
    </Table>
  </Card>
)

export default NodeDetail
