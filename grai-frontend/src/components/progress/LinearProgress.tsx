import React from "react"
import {
  Box,
  LinearProgress as BaseLinearProgress,
  Typography,
  LinearProgressPropsColorOverrides,
} from "@mui/material"
import { OverridableStringUnion } from "@mui/types"

type LinearProgressProps = {
  value: number
  color?: OverridableStringUnion<
    | "inherit"
    | "info"
    | "primary"
    | "secondary"
    | "error"
    | "success"
    | "warning",
    LinearProgressPropsColorOverrides
  >
  title?: string
  titleValue?: number
  percentage?: boolean
}

const LinearProgress: React.FC<LinearProgressProps> = ({
  value,
  color,
  title,
  titleValue,
  percentage,
}) => (
  <Box sx={{ width: "100%" }}>
    {title && (
      <Box sx={{ display: "flex" }}>
        <Typography variant="body2" color="text.secondary" sx={{ flexGrow: 1 }}>
          {title}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {titleValue ?? value}
          {percentage && "%"}
        </Typography>
      </Box>
    )}
    <Box sx={{ width: "100%" }}>
      <BaseLinearProgress
        variant="determinate"
        value={value}
        color={color ?? "info"}
      />
    </Box>
  </Box>
)

export default LinearProgress
