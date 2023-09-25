import React, { useState } from "react"
import { Add } from "@mui/icons-material"
import { Box, Button } from "@mui/material"
import CreateDeviceDialog from "./CreateDeviceDialog"
import SettingsAppBar from "../SettingsAppBar"

const TwoFactorHeader: React.FC = () => {
  const [open, setOpen] = useState(false)

  const handleOpen = () => setOpen(true)
  const handleClose = () => setOpen(false)

  return (
    <SettingsAppBar
      title="2FA Keys"
      buttons={
        <>
          <Box>
            <Button
              variant="outlined"
              startIcon={<Add />}
              onClick={handleOpen}
              sx={{ height: "48px" }}
            >
              Add 2FA Key
            </Button>
          </Box>
          <CreateDeviceDialog open={open} onClose={handleClose} />
        </>
      }
    />
  )
}
export default TwoFactorHeader
