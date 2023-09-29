import { Tooltip, TooltipProps } from "@mui/material"
import React from "react"

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
