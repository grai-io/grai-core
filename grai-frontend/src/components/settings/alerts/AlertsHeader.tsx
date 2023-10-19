import React, { useState } from "react"
import { Add } from "@mui/icons-material"
import { Box, Button } from "@mui/material"
import CreateAlertDialog from "./CreateAlertDialog"
import SettingsAppBar from "../SettingsAppBar"

type AlertsHeaderProps = {
  workspaceId: string
}

const AlertsHeader: React.FC<AlertsHeaderProps> = ({ workspaceId }) => {
  const [open, setOpen] = useState(false)

  const handleOpen = () => setOpen(true)
  const handleClose = () => setOpen(false)

  return (
    <SettingsAppBar
      title="Alerts"
      buttons={
        <>
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
        </>
      }
    />
  )
}
export default AlertsHeader
