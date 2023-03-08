import React from "react"
import { Box, Divider, Stack } from "@mui/material"
import { Error } from "components/graph/Graph"
import ResultValue from "./ResultValue"

type ReportResultProps = { errors: Error[] | null }

const ReportResult: React.FC<ReportResultProps> = ({ errors }) => {
  const failureCount = errors?.filter(error => !error.test_pass).length ?? 0
  const passCount = errors?.filter(error => error.test_pass).length ?? 0
  const total = failureCount + passCount

  return (
    <Box sx={{ px: 2 }}>
      <Divider />
      <Stack direction="row" spacing={3} sx={{ py: 2 }}>
        <ResultValue title="Failures" value={failureCount} />
        <ResultValue title="Passes" value={passCount} />
        <ResultValue title="Success Rate" percentage={passCount / total} />
      </Stack>
      <Divider />
    </Box>
  )
}

export default ReportResult
