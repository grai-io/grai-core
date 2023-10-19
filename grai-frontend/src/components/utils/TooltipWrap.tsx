import React from "react"
import { Tooltip, TooltipProps } from "@mui/material"

interface TooltipWrapProps extends TooltipProps {
  show: boolean
}

const TooltipWrap: React.FC<TooltipWrapProps> = ({
  show,
  children,
  ...rest
}) => {
  if (show) return <Tooltip {...rest}>{children}</Tooltip>

  return children
}

export default TooltipWrap
