import { Box, Card, Grid, Table, TableBody, Typography } from "@mui/material"
import React from "react"
import ConnectionDetail from "./ConnectionDetail"
import ConnectionRunDetail from "./ConnectionRunDetail"
import ConnectionRunsTable from "./ConnectionRunsTable"
import ConnectionSchedule, {
  Connection as BaseConnection,
} from "./ConnectionSchedule"

interface Run {
  id: string
  status: string
}

interface Connector {
  id: string
  name: string
  metadata: any
}

interface User {
  id: string
  first_name: string
  last_name: string
}

interface Run {
  id: string
  user: User | null
  status: string
  created_at: string
  started_at: string | null
  finished_at: string | null
}

interface Connection extends BaseConnection {
  id: string
  name: string
  namespace: string
  connector: Connector
  runs: Run[]
  last_run: Run | null
  last_successful_run: Run | null
  metadata: any
}

type ConnectionContentProps = {
  connection: Connection
}

const ConnectionContent: React.FC<ConnectionContentProps> = ({
  connection,
}) => (
  <Box sx={{ px: 2, py: 1 }}>
    <Grid container spacing={3} sx={{ py: 3 }}>
      <Grid item md={6}>
        <ConnectionDetail connection={connection} />
      </Grid>
      <Grid item md={6}>
        <Card variant="outlined" sx={{ borderRadius: 0, borderBottom: 0 }}>
          <Table>
            <TableBody>
              <ConnectionSchedule connection={connection} />
              <ConnectionRunDetail label="Last Run" run={connection.last_run} />
              <ConnectionRunDetail
                label="Last Successful Run"
                run={connection.last_successful_run}
              />
            </TableBody>
          </Table>
        </Card>
      </Grid>
    </Grid>
    <Typography variant="h6" sx={{ ml: 1 }}>
      Runs
    </Typography>
    <ConnectionRunsTable runs={connection.runs} />
  </Box>
)

export default ConnectionContent
