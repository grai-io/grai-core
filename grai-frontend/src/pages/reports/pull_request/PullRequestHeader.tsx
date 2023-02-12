import { Box } from "@mui/material"
import React from "react"
import PullRequestBreadcrumbs, {
  Repository as BaseRepository,
} from "./PullRequestBreadcrumbs"

interface Repository extends BaseRepository {}

interface PullRequest {
  reference: string
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
  </Box>
)

export default PullRequestHeader
