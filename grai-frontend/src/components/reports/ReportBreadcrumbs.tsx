import React from "react"
import { Breadcrumbs, Link, Typography } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import { Link as RouterLink } from "react-router-dom"

export interface Repository {
  owner: string
  repo: string
}

type ReportBreadcrumbsProps = {
  type: string
  repository: Repository
}

const ReportBreadcrumbs: React.FC<ReportBreadcrumbsProps> = ({
  type,
  repository,
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
      <Typography color="text.primary">{repository.repo}</Typography>
    </Breadcrumbs>
  )
}

export default ReportBreadcrumbs
