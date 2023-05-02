import React from "react"
import { Breadcrumbs, Link } from "@mui/material"
import { Link as RouterLink } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"

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
    <Breadcrumbs sx={{ mt: -1, mb: 1 }}>
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
