import React from "react"
import { Box } from "@mui/material"
import ReportBreadcrumbs, { Repository } from "./ReportBreadcrumbs"

type ReportHeaderProps = {
  type: string
  repository: Repository
}

const ReportHeader: React.FC<ReportHeaderProps> = ({ type, repository }) => (
  <Box sx={{ p: 2 }}>
    <ReportBreadcrumbs type={type} repository={repository} />
  </Box>
)

export default ReportHeader
