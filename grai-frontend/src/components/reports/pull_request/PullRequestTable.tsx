import React from "react"
import { Table, TableBody, TableCell, TableHead, TableRow } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import { Repository } from "../ReportBreadcrumbs"
import RunFailures, { Run } from "../results/RunFailures"
import RunSuccessRate from "../results/RunSuccessRate"

interface Branch {
  reference: string
}

interface Commit {
  last_successful_run: Run | null
}

interface PullRequest {
  reference: string
  title: string | null
  branch: Branch
  last_commit: Commit | null
}

type PullRequestTableProps = {
  pull_requests: PullRequest[]
  type: string
  repository: Repository
}

const PullRequestTable: React.FC<PullRequestTableProps> = ({
  pull_requests,
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
          <TableCell sx={{ textAlign: "right" }}>Failures</TableCell>
          <TableCell sx={{ textAlign: "right" }}>Success Rate</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {pull_requests.map(pull_request => (
          <TableRow
            key={pull_request.reference}
            hover
            sx={{ cursor: "pointer" }}
            onClick={() =>
              workspaceNavigate(
                `reports/${type}/${repository.owner}/${repository.repo}/pulls/${pull_request.reference}`
              )
            }
          >
            <TableCell>{pull_request.title}</TableCell>
            <TableCell>#{pull_request.reference}</TableCell>
            <TableCell>{pull_request.branch.reference}</TableCell>
            <TableCell sx={{ textAlign: "right" }}>
              <RunFailures
                run={pull_request.last_commit?.last_successful_run ?? null}
              />
            </TableCell>
            <TableCell sx={{ textAlign: "right" }}>
              <RunSuccessRate
                run={pull_request.last_commit?.last_successful_run ?? null}
              />
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}

export default PullRequestTable
