import React from "react"
import { Card, Grid, Table, TableBody } from "@mui/material"
// import { Column } from "./columns/TableColumnsTable"
import TableDependencies from "./TableDependencies"
import TableDetail from "./TableDetail"

// interface BaseTable {
//   id: string
//   display_name: string
// }

interface DataSource {
  id: string
  name: string
}
export interface Node {
  id: string
  name: string
  namespace: string
  display_name: string
  // columns: { data: Column[] }
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
          </TableBody>
        </Table>
      </Card>
    </Grid>
  </Grid>
)

export default NodeProfile
