import React from "react"
import {
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Typography,
  Tooltip,
} from "@mui/material"
import {
  durationAgo,
  runQueuedString,
  runDurationString,
} from "helpers/runDuration"
import { DateTime } from "luxon"
import { useNavigate } from "react-router-dom"
import Loading from "components/layout/Loading"
import RunStatus from "./RunStatus"

interface Connection {
  name: string
  connector: Connector
}

interface Connector {
  name: string
}

interface User {
  id: string
  first_name: string
  last_name: string
}

interface Run {
  id: string
  status: string
  connection: Connection | null
  created_at: string
  started_at: string | null
  finished_at: string | null
  user: User | null
}

type RunsTableProps = {
  runs: Run[]
  loading?: boolean
}

const RunsTable: React.FC<RunsTableProps> = ({ runs, loading }) => {
  const navigate = useNavigate()

  return (
    <Table>
      <TableHead>
        <TableRow sx={{ backgroundColor: theme => theme.palette.grey[100] }}>
          <TableCell>id</TableCell>
          <TableCell>Connection</TableCell>
          <TableCell>Connector</TableCell>
          <TableCell>User</TableCell>
          <TableCell>Status</TableCell>
          <TableCell sx={{ textAlign: "right" }}>Started</TableCell>
          <TableCell sx={{ textAlign: "right" }}>Queued</TableCell>
          <TableCell sx={{ textAlign: "right" }}>Duration</TableCell>
          <TableCell sx={{ width: 0 }} />
        </TableRow>
      </TableHead>
      <TableBody>
        {runs.map(run => (
          <TableRow
            key={run.id}
            hover
            sx={{ cursor: "pointer" }}
            onClick={() => navigate(run.id)}
          >
            <TableCell sx={{ pl: 1 }}>{run.id.slice(0, 6)}</TableCell>
            <TableCell>{run.connection?.name}</TableCell>
            <TableCell>{run.connection?.connector.name}</TableCell>
            <TableCell>{run.user?.first_name}</TableCell>
            <TableCell sx={{ py: 0 }}>
              <RunStatus run={run} size="small" sx={{ cursor: "pointer" }} />
            </TableCell>
            <TableCell sx={{ textAlign: "right" }}>
              <Tooltip
                title={DateTime.fromISO(run.created_at).toLocaleString(
                  DateTime.DATETIME_FULL_WITH_SECONDS
                )}
              >
                <Typography variant="body2">
                  {durationAgo(run.created_at)} ago
                </Typography>
              </Tooltip>
            </TableCell>
            <TableCell sx={{ textAlign: "right" }}>
              {runQueuedString(run)}
            </TableCell>
            <TableCell sx={{ textAlign: "right" }}>
              {runDurationString(run)}
            </TableCell>
          </TableRow>
        ))}
        {!loading && runs.length === 0 && (
          <TableRow>
            <TableCell colSpan={99} sx={{ textAlign: "center", py: 10 }}>
              <Typography>No runs found</Typography>
            </TableCell>
          </TableRow>
        )}
        {loading && (
          <TableRow>
            <TableCell colSpan={99}>
              <Loading />
            </TableCell>
          </TableRow>
        )}
      </TableBody>
    </Table>
  )
}

export default RunsTable
