import React from "react"
import { Refresh } from "@mui/icons-material"
import { Box, Button, Stack, Tooltip } from "@mui/material"
import { useSearchParams } from "react-router-dom"
import getRepoFromParams from "helpers/getRepoFromParams"
import BranchFilter, { Branch } from "./filters/BranchFilter"
import RepositoryFilter from "./filters/RepositoryFilter"

interface PullRequest {
  reference: string
  title: string | null
}

interface Repository {
  type: string
  owner: string
  repo: string
  branches: { data: Branch[] }
  pull_requests: { data: PullRequest[] }
}

interface Workspace {
  repositories: { data: Repository[] }
}

type ReportFilterProps = {
  workspace: Workspace | null
  onRefresh?: () => void
}

const ReportFilter: React.FC<ReportFilterProps> = ({
  workspace,
  onRefresh,
}) => {
  const [searchParams] = useSearchParams()
  const { owner, repo } = getRepoFromParams(searchParams)

  const repositories = workspace?.repositories.data

  const branches = owner
    ? workspace?.repositories.data.find(
        repository => repository.owner === owner && repository.repo === repo
      )?.branches.data
    : workspace?.repositories.data.reduce<Branch[]>(
        (res, repository) => res.concat(repository.branches.data),
        []
      )

  return (
    <Box sx={{ display: "flex", mb: "24px" }}>
      <Stack direction="row" spacing={1} sx={{ flexGrow: 1 }}>
        <RepositoryFilter
          repositories={repositories ?? []}
          disabled={!repositories}
        />
        <BranchFilter branches={branches ?? []} disabled={!branches} />
      </Stack>
      {onRefresh && (
        <Box>
          <Tooltip title="Refresh reports">
            <Button
              variant="outlined"
              onClick={onRefresh}
              sx={{ width: 40, height: 40, minWidth: 0 }}
            >
              <Refresh />
            </Button>
          </Tooltip>
        </Box>
      )}
    </Box>
  )
}

export default ReportFilter
