import {
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Typography,
} from "@mui/material"
import React from "react"
import theme from "theme"

interface User {
  id: string
  first_name: string
  last_name: string
}

interface Run {
  id: string
  user: User | null
  status: string
  started_at: string
}

type ConnectionRunsTableProps = {
  runs: Run[]
}

const ConnectionRunsTable: React.FC<ConnectionRunsTableProps> = ({ runs }) => (
  <Table sx={{ mt: 1 }}>
    <TableHead sx={{ backgroundColor: theme => theme.palette.grey[100] }}>
      <TableRow>
        <TableCell sx={{ width: 0 }} />
        <TableCell>id</TableCell>
        <TableCell>User</TableCell>
        <TableCell>Status</TableCell>
        <TableCell>Started</TableCell>
        <TableCell>Queued</TableCell>
        <TableCell>Duration</TableCell>
        <TableCell />
      </TableRow>
    </TableHead>
    <TableBody>
      {runs.map((run, index) => (
        <TableRow key={run.id}>
          <TableCell sx={{ color: theme.palette.grey[500], pr: 0 }}>
            {index}
          </TableCell>
          <TableCell sx={{ pl: 1 }}>{run.id.slice(0, 6)}</TableCell>
          <TableCell>{run.user?.first_name}</TableCell>
          <TableCell>{run.status}</TableCell>
          <TableCell>{run.started_at}</TableCell>
          <TableCell />
          <TableCell />
          <TableCell />
        </TableRow>
      ))}
      {runs.length === 0 && (
        <TableRow>
          <TableCell colSpan={99} sx={{ textAlign: "center", py: 10 }}>
            <Typography>No runs found</Typography>
          </TableCell>
        </TableRow>
      )}
    </TableBody>
  </Table>
)

export default ConnectionRunsTable
