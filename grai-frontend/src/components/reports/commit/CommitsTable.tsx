import React from "react"
import { Table, TableHead, TableRow, TableCell, TableBody } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import { Repository } from "../ReportBreadcrumbs"
import RunFailures, { Run } from "../results/RunFailures"
import RunSuccessRate from "../results/RunSuccessRate"

interface Branch {
  reference: string
}

interface PullRequest {
  reference: string
  title: string | null
}

interface Commit {
  reference: string
  title: string | null
  branch: Branch
  pull_request: PullRequest | null
  last_successful_run: Run | null
}

type CommitsTableProps = {
  commits: Commit[]
  type: string
  repository: Repository
}

const CommitsTable: React.FC<CommitsTableProps> = ({
  commits,
  type,
  repository,
}) => {
  const { workspaceNavigate } = useWorkspace()

  return (
    <Table>
      <TableHead>
        <TableRow sx={{ backgroundColor: theme => theme.palette.grey[100] }}>
          <TableCell>Name</TableCell>
          <TableCell />
          <TableCell>Branch</TableCell>
          <TableCell>Pull Request</TableCell>
          <TableCell sx={{ textAlign: "right" }}>Failures</TableCell>
          <TableCell sx={{ textAlign: "right" }}>Success Rate</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {commits.map(commit => (
          <TableRow
            key={commit.reference}
            hover
            sx={{ cursor: "pointer" }}
            onClick={() =>
              workspaceNavigate(
                `reports/${type}/${repository.owner}/${repository.repo}/commits/${commit.reference}`
              )
            }
          >
            <TableCell>{commit.title}</TableCell>
            <TableCell>{commit.reference.slice(0, 7)}</TableCell>
            <TableCell>{commit.branch.reference}</TableCell>
            <TableCell>{commit.pull_request?.title}</TableCell>
            <TableCell sx={{ textAlign: "right" }}>
              <RunFailures run={commit.last_successful_run} />
            </TableCell>
            <TableCell sx={{ textAlign: "right" }}>
              <RunSuccessRate run={commit.last_successful_run} />
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}

export default CommitsTable
