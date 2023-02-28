import React from "react"
import { Table, TableBody, TableCell, TableHead, TableRow } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import { Repository } from "../ReportBreadcrumbs"

interface Branch {
  reference: string
}

interface PullRequest {
  reference: string
  title: string | null
  branch: Branch
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
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}

export default PullRequestTable
