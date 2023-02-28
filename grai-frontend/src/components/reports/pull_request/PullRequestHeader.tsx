import React from "react"
import { CallSplit, OpenInNew } from "@mui/icons-material"
import { Box, Link, Typography } from "@mui/material"
import { durationAgo } from "helpers/runDuration"
import PullRequestBreadcrumbs, {
  Repository as BaseRepository,
} from "./PullRequestBreadcrumbs"

interface Repository extends BaseRepository {}

interface Commit {
  created_at: string
}

interface Branch {
  reference: string
}

interface PullRequest {
  reference: string
  title: string | null
  last_commit: Commit | null
  branch: Branch
}

type PullRequestHeaderProps = {
  type: string
  repository: Repository
  pullRequest: PullRequest
}

const PullRequestHeader: React.FC<PullRequestHeaderProps> = ({
  type,
  repository,
  pullRequest,
}) => (
  <Box sx={{ p: 2 }}>
    <PullRequestBreadcrumbs
      type={type}
      repository={repository}
      reference={pullRequest.reference}
    />
    <Box sx={{ mt: 1 }}>
      <Typography variant="h6">{pullRequest.title}</Typography>
    </Box>
    <Box sx={{ display: "flex" }}>
      <Typography variant="body2" sx={{ display: "flex" }}>
        {pullRequest.last_commit?.created_at &&
          `about ${durationAgo(
            pullRequest.last_commit.created_at,
            1,
            true
          )} ago `}
        <Link
          href={`https://github.com/${repository.owner}/${repository.repo}/pull/${pullRequest.reference}`}
          target="_blank"
          underline="hover"
          sx={{ display: "flex", alignItems: "center", ml: 0.5 }}
        >
          <span>#{pullRequest.reference}</span>
          <OpenInNew sx={{ fontSize: 15, ml: 0.25 }} />
        </Link>
      </Typography>
      <Typography
        variant="body2"
        sx={{ ml: 1, display: "flex", alignItems: "center" }}
      >
        <CallSplit sx={{ fontSize: 15, mx: 0.25 }} />
        {pullRequest.branch.reference}
      </Typography>
    </Box>
  </Box>
)

export default PullRequestHeader
