import React from "react"
import { Table, TableHead, TableRow, TableCell, TableBody } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import { Repository } from "../ReportBreadcrumbs"

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
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}

export default CommitsTable
