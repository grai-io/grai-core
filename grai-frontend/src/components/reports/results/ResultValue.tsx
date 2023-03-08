import React from "react"
import { Box, Typography } from "@mui/material"

type ResultValueProps = {
  title: string
  value?: number
  percentage?: number
}

const ResultValue: React.FC<ResultValueProps> = ({
  title,
  value,
  percentage,
}) => (
  <Box>
    <Typography variant="body2" sx={{ mb: 1 }}>
      {title}
    </Typography>
    {value !== undefined && (
      <Typography variant="h6" sx={{ display: "inline", mr: 2 }}>
        {value}
      </Typography>
    )}
    {percentage !== undefined && (
      <Typography variant="h6" sx={{ display: "inline", mr: 2 }}>
        {(percentage * 100).toFixed(2)}%
      </Typography>
    )}
  </Box>
)

export default ResultValue
