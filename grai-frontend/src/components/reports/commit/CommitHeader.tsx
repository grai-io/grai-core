import React from "react"
import { CallSplit, OpenInNew } from "@mui/icons-material"
import { Box, Link, Typography } from "@mui/material"
import { durationAgo } from "helpers/runDuration"
import CommitBreadcrumbs, {
  Repository as BaseRepository,
} from "./CommitBreadcrumbs"

interface Repository extends BaseRepository {}

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
  created_at: string
  branch: Branch
  pull_request: PullRequest | null
}

type CommitHeaderProps = {
  type: string
  repository: Repository
  commit: Commit
}

const CommitHeader: React.FC<CommitHeaderProps> = ({
  type,
  repository,
  commit,
}) => (
  <Box sx={{ p: 2 }}>
    <CommitBreadcrumbs
      type={type}
      repository={repository}
      reference={commit.reference}
    />
    <Box sx={{ mt: 1 }}>
      <Typography variant="h6">{commit.title}</Typography>
    </Box>
    <Box sx={{ display: "flex" }}>
      <Typography variant="body2" sx={{ display: "flex" }}>
        {`about ${durationAgo(commit.created_at, 1, true)} ago `}
        <Link
          href={
            commit.pull_request
              ? `https://github.com/${repository.owner}/${repository.repo}/pull/${commit.pull_request.reference}/commits/${commit.reference}`
              : `https://github.com/${repository.owner}/${repository.repo}/tree/${commit.reference}`
          }
          target="_blank"
          underline="hover"
          sx={{ display: "flex", alignItems: "center", ml: 0.5 }}
        >
          <span>#{commit.reference.slice(0, 7)}</span>
          <OpenInNew sx={{ fontSize: 15, ml: 0.25 }} />
        </Link>
      </Typography>
      <Typography
        variant="body2"
        sx={{ ml: 1, display: "flex", alignItems: "center" }}
      >
        <CallSplit sx={{ fontSize: 15, mx: 0.25 }} />
        {commit.branch.reference}
      </Typography>
    </Box>
  </Box>
)

export default CommitHeader
