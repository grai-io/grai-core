import React from "react"
import { CallSplit, OpenInNew } from "@mui/icons-material"
import { Box, Link, Typography } from "@mui/material"
import { durationAgo } from "helpers/runDuration"
import RunBreadcrumbs, { Repository } from "./RunBreadcrumbs"

interface PullRequest {
  reference: string
  title: string | null
}

interface Branch {
  reference: string
}

interface Commit {
  repository: Repository
  branch: Branch
  pull_request: PullRequest | null
}

interface Run {
  id: string
  commit: Commit | null
  created_at: string
}

type ReportRunHeaderProps = {
  run: Run
}

const ReportRunHeader: React.FC<ReportRunHeaderProps> = ({ run }) => {
  return (
    <Box sx={{ p: 2 }}>
      {run.commit && <RunBreadcrumbs repository={run.commit.repository} />}
      <Typography variant="h6">Run {run.id.slice(0, 6)}</Typography>
      <Box sx={{ display: "flex" }}>
        <Typography variant="body2" sx={{ display: "flex" }}>
          {run.created_at &&
            `about ${durationAgo(run.created_at, 1, true)} ago `}
          {run.commit?.pull_request && (
            <Link
              href={`https://github.com/${run.commit.repository.owner}/${run.commit.repository.repo}/pull/${run.commit.pull_request.reference}`}
              target="_blank"
              underline="hover"
              sx={{ display: "flex", alignItems: "center", ml: 0.5 }}
            >
              <span>
                {run.commit.pull_request.title} #
                {run.commit.pull_request.reference}
              </span>
              <OpenInNew sx={{ fontSize: 15, ml: 0.25 }} />
            </Link>
          )}
        </Typography>
        {run.commit?.branch && (
          <Typography
            variant="body2"
            sx={{ ml: 1, display: "flex", alignItems: "center" }}
          >
            <CallSplit sx={{ fontSize: 15, mx: 0.25 }} />
            {run.commit.branch.reference}
          </Typography>
        )}
      </Box>
    </Box>
  )
}

export default ReportRunHeader
