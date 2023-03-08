import React from "react"
import { AccountCircle } from "@mui/icons-material"
import {
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Typography,
  Tooltip,
  Avatar,
  Box,
} from "@mui/material"
import { durationAgo } from "helpers/runDuration"
import useWorkspace from "helpers/useWorkspace"
import { DateTime } from "luxon"
import Loading from "components/layout/Loading"
import RunStatus from "components/runs/RunStatus"
import RunFailures, { Run as RunWithMetadata } from "./results/RunFailures"
import RunSuccessRate from "./results/RunSuccessRate"

interface Branch {
  reference: string
}

interface PullRequest {
  reference: string
  title: string | null
}

interface Repository {
  type: string
  owner: string
  repo: string
}

interface Commit {
  reference: string
  title: string | null
  branch: Branch
  pull_request: PullRequest | null
  repository: Repository
}

interface Connection {
  name: string
  temp: boolean
  connector: Connector
}

interface Connector {
  name: string
  icon: string | null
}

interface User {
  id: string
  first_name: string
  last_name: string
}

interface Run extends RunWithMetadata {
  id: string
  status: string
  connection: Connection
  created_at: string
  started_at: string | null
  finished_at: string | null
  user: User | null
  commit: Commit | null
}

type ReportsTableProps = {
  runs: Run[] | null
  loading?: boolean
}

const ReportsTable: React.FC<ReportsTableProps> = ({ runs, loading }) => {
  const { workspaceNavigate } = useWorkspace()

  const getLink = (run: Run): string =>
    run.commit
      ? `reports/${run.commit.repository.type}/${run.commit.repository.owner}/reports/${run.id}`
      : `reports/${run.id}`

  const handleNavigate = (run: Run) => () => workspaceNavigate(getLink(run))

  return (
    <Table>
      <TableHead>
        <TableRow sx={{ backgroundColor: theme => theme.palette.grey[100] }}>
          <TableCell>id</TableCell>
          <TableCell>Connection</TableCell>
          <TableCell>Repository</TableCell>
          <TableCell>Trigger</TableCell>
          <TableCell>Status</TableCell>
          <TableCell sx={{ textAlign: "right" }}>Started</TableCell>
          <TableCell sx={{ textAlign: "right" }}>Failures</TableCell>
          <TableCell sx={{ textAlign: "right" }}>Success Rate</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {runs?.map(run => (
          <TableRow
            key={run.id}
            hover
            sx={{ cursor: "pointer" }}
            onClick={handleNavigate(run)}
          >
            <TableCell sx={{ pl: 1 }}>{run.id.slice(0, 6)}</TableCell>
            <TableCell sx={{ py: 0 }}>
              <Box sx={{ display: "flex" }}>
                {run.connection.connector.icon && (
                  <Avatar
                    src={run.connection.connector.icon}
                    sx={{
                      width: 24,
                      height: 24,
                      mr: 1,
                      filter: run.connection.temp
                        ? "grayscale(100%)"
                        : undefined,
                    }}
                  />
                )}
                {run.connection.temp ? (
                  <Typography
                    variant="body2"
                    sx={{ color: theme => theme.palette.grey[500] }}
                  >
                    {run.connection.connector.name}
                  </Typography>
                ) : (
                  <Typography variant="body2">{run.connection.name}</Typography>
                )}
              </Box>
            </TableCell>
            <TableCell sx={{ py: 0 }}>
              {run.commit && (
                <Box sx={{ display: "flex" }}>
                  <Avatar
                    src="/images/github-logo.png"
                    sx={{ width: 24, height: 24, mr: 1 }}
                  />

                  <Typography variant="body2">
                    {run.commit.repository.owner}/{run.commit.repository.repo}
                  </Typography>
                </Box>
              )}
            </TableCell>
            <TableCell sx={{ py: 0 }}>
              {run.commit ? (
                <Box sx={{ display: "flex" }}>
                  {run.commit.pull_request ? (
                    <>
                      {run.commit.pull_request.title} #
                      {run.commit.pull_request.reference}
                    </>
                  ) : (
                    <>{run.commit.branch.reference.slice(0, 7)}</>
                  )}
                </Box>
              ) : (
                <Box sx={{ display: "flex" }}>
                  <AccountCircle sx={{ mr: 1 }} />
                  <Typography variant="body2">
                    {run.user?.first_name}
                  </Typography>
                </Box>
              )}
            </TableCell>
            <TableCell sx={{ py: 0 }}>
              <RunStatus run={run} size="small" sx={{ cursor: "pointer" }} />
            </TableCell>
            <TableCell sx={{ textAlign: "right" }}>
              <Box>
                <Tooltip
                  title={DateTime.fromISO(run.created_at).toLocaleString(
                    DateTime.DATETIME_FULL_WITH_SECONDS
                  )}
                >
                  <Typography variant="body2">
                    {durationAgo(run.created_at, 1)} ago
                  </Typography>
                </Tooltip>
              </Box>
            </TableCell>
            <TableCell sx={{ textAlign: "right" }}>
              <RunFailures run={run} />
            </TableCell>
            <TableCell sx={{ textAlign: "right" }}>
              <RunSuccessRate run={run} />
            </TableCell>
          </TableRow>
        ))}
        {!loading && runs?.length === 0 && (
          <TableRow>
            <TableCell colSpan={99} sx={{ textAlign: "center", py: 10 }}>
              <Typography>No reports found</Typography>
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

export default ReportsTable
