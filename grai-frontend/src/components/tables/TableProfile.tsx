import React from "react"
import { Card, Grid, Table, TableBody } from "@mui/material"
import TableColumns from "./columns/TableColumns"
import { Column } from "./columns/TableColumnsTable"
import TableDependencies from "./TableDependencies"
import TableDetail from "./TableDetail"

interface BaseTable {
  id: string
  display_name: string
}

export interface TableInterface {
  id: string
  name: string
  namespace: string
  data_source: string
  display_name: string
  columns: Column[]
  metadata: any | null
  source_tables: BaseTable[]
  destination_tables: BaseTable[]
}

type TableProfileProps = {
  table: TableInterface
}

const TableProfile: React.FC<TableProfileProps> = ({ table }) => (
  <>
    <Grid container spacing={3} sx={{ pt: 3 }}>
      <Grid item md={6}>
        <TableDetail table={table} />
      </Grid>
      <Grid item md={6}>
        <Card variant="outlined" sx={{ borderRadius: 0, borderBottom: 0 }}>
          <Table>
            <TableBody>
              <TableDependencies
                label="Upstream dependencies"
                dependencies={table.destination_tables}
              />
              <TableDependencies
                label="Downstream dependencies"
                dependencies={table.source_tables}
              />
            </TableBody>
          </Table>
        </Card>
      </Grid>
    </Grid>
    <TableColumns columns={table.columns} />
  </>
)

export default TableProfile
