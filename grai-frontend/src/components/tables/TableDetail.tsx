import React from "react"
import { Card, Chip, Stack, Table, TableBody } from "@mui/material"
import { JsonView, defaultStyles } from "react-json-view-lite"
import NodeDetailRow from "components/layout/NodeDetailRow"
import "react-json-view-lite/dist/index.css"

type Metadata = { [k: string]: any } | null

interface TableInterface {
  name: string
  namespace: string
  // data_source: string
  metadata?: Metadata
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
        {/* <NodeDetailRow label="Data Source" value={table.data_source} /> */}
        <NodeDetailRow label="Tags">
          <Stack direction="row" spacing={1}>
            {(table.metadata?.grai?.tags ?? []).map((tag: string) => (
              <Chip key={tag} label={tag} />
            ))}
          </Stack>
        </NodeDetailRow>
        <NodeDetailRow label="Metadata">
          {table.metadata && (
            <JsonView
              data={table.metadata}
              shouldInitiallyExpand={level => level < 1}
              style={{ ...defaultStyles, container: "" }}
            />
          )}
        </NodeDetailRow>
      </TableBody>
    </Table>
  </Card>
)

export default TableDetail
