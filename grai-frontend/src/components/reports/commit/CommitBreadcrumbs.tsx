import React from "react"
import { Breadcrumbs, Link, Typography } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import { Link as RouterLink } from "react-router-dom"

export interface Repository {
  owner: string
  repo: string
}

type CommitBreadcrumbsProps = {
  type: string
  repository: Repository
  reference: string
}

const CommitBreadcrumbs: React.FC<CommitBreadcrumbsProps> = ({
  type,
  repository,
  reference,
}) => {
  const { routePrefix } = useWorkspace()

  const routeStart = `${routePrefix}/reports/${type}`

  return (
    <Breadcrumbs>
      <Link
        underline="hover"
        color="inherit"
        component={RouterLink}
        to={`${routeStart}/${repository.owner}`}
      >
        {repository.owner}
      </Link>
      <Link
        underline="hover"
        color="inherit"
        component={RouterLink}
        to={`${routeStart}/${repository.owner}/${repository.repo}`}
      >
        {repository.repo}
      </Link>
      <Link
        underline="hover"
        color="inherit"
        component={RouterLink}
        to={`${routeStart}/${repository.owner}/${repository.repo}`}
      >
        commits
      </Link>
      <Typography color="text.primary">{reference.slice(0, 7)}</Typography>
    </Breadcrumbs>
  )
}

export default CommitBreadcrumbs
