import React from "react"
import { Breadcrumbs, Link } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import { Link as RouterLink } from "react-router-dom"

export interface Repository {
  type: string
  owner: string
  repo: string
}

type RunBreadcrumbsProps = {
  repository: Repository
}

const RunBreadcrumbs: React.FC<RunBreadcrumbsProps> = ({ repository }) => {
  const { routePrefix } = useWorkspace()

  const routeStart = `${routePrefix}/reports/${repository.type}`

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
    </Breadcrumbs>
  )
}

export default RunBreadcrumbs
