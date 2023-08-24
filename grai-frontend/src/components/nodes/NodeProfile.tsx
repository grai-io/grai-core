import React from "react"
import { Card, Grid, Stack, Table, TableBody } from "@mui/material"
// import { Column } from "./columns/TableColumnsTable"
import TableDependencies from "./TableDependencies"
import TableDetail from "./TableDetail"
import NodeDetailRow from "components/layout/NodeDetailRow"
import LinearProgress from "components/progress/LinearProgress"
import BarChart from "./BarChart"
// interface BaseTable {
//   id: string
//   display_name: string
// }

interface Column {
  id: string
}
interface DataSource {
  id: string
  name: string
}
export interface Node {
  id: string
  name: string
  namespace: string
  display_name: string
  columns: { data: Column[] }
  metadata: any | null
  // source_tables: { data: BaseTable[] }
  // destination_tables: { data: BaseTable[] }
  data_sources: { data: DataSource[] }
}

type NodeProfileProps = {
  node: Node
}

const NodeProfile: React.FC<NodeProfileProps> = ({ node }) => (
  <Grid container spacing={3}>
    <Grid item md={6}>
      <TableDetail table={node} />
    </Grid>
    <Grid item md={6}>
      <Card variant="outlined" sx={{ borderRadius: 0, borderBottom: 0 }}>
        <Table>
          <TableBody>
            {/* <TableDependencies
              label="Upstream dependencies"
              dependencies={node.destination_tables.data}
            />
            <TableDependencies
              label="Downstream dependencies"
              dependencies={node.source_tables.data}
            /> */}
            <TableDependencies
              label="Sources"
              dependencies={node.data_sources.data}
              routePrefix="sources"
            />
            {node.metadata.grai.node_type === "Column" && (
              <NodeDetailRow label="Data">
                <Stack direction="column" spacing={1}>
                  <LinearProgress
                    value={50}
                    title="credit-card"
                    titleValue={25}
                  />
                  <LinearProgress value={30} title="cash" titleValue={15} />
                  <LinearProgress value={10} title="bnpl" titleValue={5} />
                  <BarChart />
                </Stack>
              </NodeDetailRow>
            )}
          </TableBody>
        </Table>
      </Card>
    </Grid>
  </Grid>
)

export default NodeProfile
