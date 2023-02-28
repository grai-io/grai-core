import React from "react"
import { Box, lighten } from "@mui/material"

type TestsSummaryProps = {
  errorCount: number
  passCount: number
}

const TestsSummary: React.FC<TestsSummaryProps> = ({
  errorCount,
  passCount,
}) => (
  <Box sx={{ display: "flex" }}>
    {errorCount > 0 && (
      <Box
        sx={{
          px: 2,
          py: 1,
          backgroundColor: theme => lighten(theme.palette.error.light, 0.6),
          "&:hover": {
            backgroundColor: theme => lighten(theme.palette.error.light, 0.3),
          },
        }}
      >
        {errorCount}
      </Box>
    )}
    {passCount > 0 && (
      <Box
        sx={{
          px: 2,
          py: 1,
          backgroundColor: theme => lighten(theme.palette.success.light, 0.6),
          "&:hover": {
            backgroundColor: theme => lighten(theme.palette.success.light, 0.3),
          },
        }}
      >
        {passCount}
      </Box>
    )}
  </Box>
)

export default TestsSummary
