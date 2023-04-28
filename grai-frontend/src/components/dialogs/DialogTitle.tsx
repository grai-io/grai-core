import React from "react"
import { ChevronLeft, Close } from "@mui/icons-material"
import { DialogTitle as BaseTitle, IconButton, Tooltip } from "@mui/material"

export interface DialogTitleProps {
  children?: React.ReactNode
  onClose?: (event: {}, reason: "backdropClick" | "escapeKeyDown") => void
  onBack?: () => void
}

const DialogTitle: React.FC<DialogTitleProps> = ({
  children,
  onClose,
  onBack,
  ...other
}) => {
  const handleClose = () => onClose && onClose({}, "backdropClick")

  return (
    <BaseTitle sx={{ m: 0, p: 2 }} {...other}>
      {onBack && (
        <Tooltip title="Back">
          <IconButton
            aria-label="back"
            onClick={onBack}
            sx={{
              // position: "absolute",
              // right: 8,
              // top: 8,
              mr: 1,
              color: theme => theme.palette.grey[500],
            }}
          >
            <ChevronLeft />
          </IconButton>
        </Tooltip>
      )}
      {children}
      {onClose && (
        <Tooltip title="Close">
          <IconButton
            aria-label="close"
            onClick={handleClose}
            sx={{
              position: "absolute",
              right: 8,
              top: 8,
              color: theme => theme.palette.grey[500],
            }}
          >
            <Close />
          </IconButton>
        </Tooltip>
      )}
    </BaseTitle>
  )
}

export default DialogTitle
