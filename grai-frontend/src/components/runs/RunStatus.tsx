import React, { JSXElementConstructor, ReactElement } from "react"
import { Check, Close, HourglassEmpty } from "@mui/icons-material"
import {
  Box,
  Chip,
  ChipPropsVariantOverrides,
  CircularProgress,
  SxProps,
  Theme,
} from "@mui/material"
import { OverridableStringUnion } from "@mui/types"
import useWorkspace from "helpers/useWorkspace"

type Status = {
  label?: string
  icon?: ReactElement<any, string | JSXElementConstructor<any>>
  color?:
    | "default"
    | "primary"
    | "secondary"
    | "error"
    | "info"
    | "success"
    | "warning"
}

interface Run {
  id: string
  status: string
}

type RunStatusProps = {
  run: Run
  variant?: OverridableStringUnion<
    "filled" | "outlined",
    ChipPropsVariantOverrides
  >
  size?: "small" | "medium"
  link?: boolean
  onClick?: () => void
  sx?: SxProps<Theme>
}

const RunStatus: React.FC<RunStatusProps> = ({
  run,
  variant = "outlined",
  size,
  link,
  onClick,
  sx,
}) => {
  const { workspaceNavigate } = useWorkspace()

  const handleNavigate = () => workspaceNavigate(`runs/${run.id}`)

  const handleClick = onClick ? onClick : link ? handleNavigate : undefined

  const status: { [key: string]: Status } = {
    queued: {
      label: "Queued",
      icon: <HourglassEmpty />,
    },
    running: {
      label: "Running",
      icon: (
        <Box sx={{ px: 0.5 }}>
          <CircularProgress size={size === "small" ? "0.8rem" : "1.2rem"} />
        </Box>
      ),
      color: "default",
    },
    success: {
      label: "Success",
      icon: <Check />,
      color: "success",
    },
    error: {
      label: "Error",
      icon: <Close />,
      color: "error",
    },
  }

  return (
    <Chip
      label={run.status}
      variant={variant}
      size={size}
      onClick={handleClick}
      sx={sx}
      {...status[run.status]}
    />
  )
}

export default RunStatus
