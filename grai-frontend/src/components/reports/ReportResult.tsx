import React from "react"
import { Stack, Typography } from "@mui/material"
import { ResultError } from "components/graph/GraphComponent"

type ReportResultProps = { errors: ResultError[] | null }

const ReportResult: React.FC<ReportResultProps> = ({ errors }) => {
  const failureCount = errors?.filter(error => !error.test_pass).length ?? 0
  const passCount = errors?.filter(error => error.test_pass).length ?? 0
  const total = failureCount + passCount

  return (
    <Stack direction="row" spacing={1}>
      <Typography>Failures</Typography>
      <Typography sx={{ mr: 3 }}>{failureCount}</Typography>
      <Typography>Passes</Typography>
      <Typography sx={{ mr: 3 }}>{passCount}</Typography>
      <Typography>Success Rate</Typography>
      <Typography sx={{ mr: 3 }}>
        {total > 0 ? ((passCount / total) * 100).toFixed(2) + "%" : "-"}
      </Typography>
    </Stack>
  )
}

export default ReportResult
