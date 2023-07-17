import React from "react"
import {
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Typography,
} from "@mui/material"
import theme from "theme"
import useWorkspace from "helpers/useWorkspace"
import RunDuration from "components/runs/RunDuration"
import RunQueued from "components/runs/RunQueued"
import RunStarted from "components/runs/RunStarted"
import RunStatus from "components/runs/RunStatus"

interface User {
  id: string
  first_name: string
  last_name: string
}

export interface Run {
  id: string
  user: User | null
  status: string
  created_at: string
  started_at: string | null
  finished_at: string | null
}

type ConnectionRunsTableProps = {
  runs: { data: Run[] }
}

const ConnectionRunsTable: React.FC<ConnectionRunsTableProps> = ({ runs }) => {
  const { workspaceNavigate } = useWorkspace()

  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell sx={{ width: 0 }} />
          <TableCell>id</TableCell>
          <TableCell>User</TableCell>
          <TableCell>Status</TableCell>
          <TableCell sx={{ textAlign: "right", width: "350px" }}>
            Started
          </TableCell>
          <TableCell sx={{ textAlign: "right" }}>Queued</TableCell>
          <TableCell sx={{ textAlign: "right" }}>Duration</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {runs.data.map((run, index) => (
          <TableRow
            key={run.id}
            hover
            sx={{ cursor: "pointer" }}
            onClick={() => workspaceNavigate(`runs/${run.id}`)}
          >
            <TableCell sx={{ color: theme.palette.grey[500], pr: 0 }}>
              {index}
            </TableCell>
            <TableCell sx={{ pl: 1 }}>{run.id.slice(0, 6)}</TableCell>
            <TableCell>{run.user?.first_name}</TableCell>
            <TableCell sx={{ py: 0 }}>
              <RunStatus run={run} size="small" sx={{ cursor: "pointer" }} />
            </TableCell>
            <TableCell sx={{ textAlign: "right" }}>
              <RunStarted run={run} />
            </TableCell>
            <TableCell sx={{ textAlign: "right" }}>
              <RunQueued run={run} />
            </TableCell>
            <TableCell sx={{ textAlign: "right" }}>
              <RunDuration run={run} />
            </TableCell>
          </TableRow>
        ))}
        {runs.data.length === 0 && (
          <TableRow>
            <TableCell colSpan={99} sx={{ textAlign: "center", py: 10 }}>
              <Typography>No runs found</Typography>
            </TableCell>
          </TableRow>
        )}
      </TableBody>
    </Table>
  )
}

export default ConnectionRunsTable
