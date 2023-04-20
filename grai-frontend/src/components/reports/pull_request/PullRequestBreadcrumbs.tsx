import React from "react"
import { Breadcrumbs, Link, Typography } from "@mui/material"
import { Link as RouterLink } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"

export interface Repository {
  owner: string
  repo: string
}

type PullRequestBreadcrumbsProps = {
  type: string
  repository: Repository
  reference: string
}

const PullRequestBreadcrumbs: React.FC<PullRequestBreadcrumbsProps> = ({
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
        to={`${routeStart}/${repository.owner}/${repository.repo}/pulls`}
      >
        pulls
      </Link>
      <Typography color="text.primary">{reference}</Typography>
    </Breadcrumbs>
  )
}

export default PullRequestBreadcrumbs
