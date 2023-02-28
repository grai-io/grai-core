import React from "react"
import { Stack } from "@mui/material"
import getRepoFromParams from "helpers/getRepoFromParams"
import { useSearchParams } from "react-router-dom"
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
  branches: Branch[]
  pull_requests: PullRequest[]
}

interface Workspace {
  repositories: Repository[]
}

type ReportFilterProps = {
  workspace: Workspace | null
}

const ReportFilter: React.FC<ReportFilterProps> = ({ workspace }) => {
  const [searchParams] = useSearchParams()
  const { owner, repo } = getRepoFromParams(searchParams)

  const repositories = workspace?.repositories

  const branches = owner
    ? workspace?.repositories.find(
        repository => repository.owner === owner && repository.repo === repo
      )?.branches
    : workspace?.repositories.reduce<Branch[]>(
        (res, repository) => res.concat(repository.branches),
        []
      )

  return (
    <Stack direction="row" spacing={1}>
      <RepositoryFilter
        repositories={repositories ?? []}
        disabled={!repositories}
      />
      <BranchFilter branches={branches ?? []} disabled={!branches} />
    </Stack>
  )
}

export default ReportFilter
