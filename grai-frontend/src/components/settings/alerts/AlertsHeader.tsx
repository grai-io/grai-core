import React, { useState } from "react"
import { Add } from "@mui/icons-material"
import { Box, Button, Typography } from "@mui/material"
import CreateAlertDialog from "./CreateAlertDialog"

type AlertsHeaderProps = {
  workspaceId: string
}

const AlertsHeader: React.FC<AlertsHeaderProps> = ({ workspaceId }) => {
  const [open, setOpen] = useState(false)

  const handleOpen = () => setOpen(true)
  const handleClose = () => setOpen(false)

  return (
    <Box sx={{ display: "flex", mb: 3 }}>
      <Typography variant="h5" sx={{ flexGrow: 1 }}>
        Alerts
      </Typography>
      <Box>
        <Button variant="outlined" startIcon={<Add />} onClick={handleOpen}>
          Add alert
        </Button>
      </Box>
      <CreateAlertDialog
        workspaceId={workspaceId}
        open={open}
        onClose={handleClose}
      />
    </Box>
  )
}
export default AlertsHeader
