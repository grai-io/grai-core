import {
  Card,
  Grid,
  Typography,
  Table,
  TableBody,
  Stack,
  Button,
  Box,
} from "@mui/material"
import React from "react"
// import TableColumns from "../tables/TableColumns"
// import TableDetail from "../tables/TableDetail"
// import { Edge, Node as NodeType } from "helpers/graph"
// import TableDetailRow from "../tables/TableDetailRow"
import { Link, useParams } from "react-router-dom"
import TableColumns from "./TableColumns"
import TableDetail from "./TableDetail"

interface Column {
  id: string
  name: string
  display_name: string
}

export interface Table {
  id: string
  name: string
  namespace: string
  data_source: string
  display_name: string
  columns: Column[]
  metadata: any
}

type TableProfileProps = {
  table: Table
}

const TableProfile: React.FC<TableProfileProps> = ({ table }) => {
  const { workspaceId } = useParams()

  return (
    <>
      <Grid container spacing={3} sx={{ pt: 3 }}>
        <Grid item md={6}>
          <TableDetail table={table} />
        </Grid>
        <Grid item md={6}>
          {/* <Card variant="outlined" sx={{ borderRadius: 0, borderBottom: 0 }}>
            <Table>
              <TableBody>
                <TableDetailRow label="Upstream dependencies">
                  {table.destinationTables.length > 0 ? (
                    <Stack>
                      {table.destinationTables?.map(table => (
                        <Box key={table.id}>
                          <Button
                            component={Link}
                            to={`/workspaces/${workspaceId}/tables/${table.id}`}
                          >
                            {table.display_name}
                          </Button>
                        </Box>
                      ))}
                    </Stack>
                  ) : (
                    <Typography variant="body2">None</Typography>
                  )}
                </TableDetailRow>
                <TableDetailRow label="Downstream dependencies">
                  {table.sourceTables.length > 0 ? (
                    <Stack>
                      {table.sourceTables.map(table => (
                        <Box key={table.id}>
                          <Button
                            component={Link}
                            to={`/workspaces/${workspaceId}/tables/${table.id}`}
                          >
                            {table.display_name}
                          </Button>
                        </Box>
                      ))}
                    </Stack>
                  ) : (
                    <Typography variant="body2">None</Typography>
                  )}
                </TableDetailRow>
              </TableBody>
            </Table>
          </Card> */}
        </Grid>
      </Grid>
      <TableColumns columns={table.columns} />
    </>
  )
}

export default TableProfile
