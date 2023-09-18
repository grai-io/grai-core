import React, { useState } from "react"
import { Add } from "@mui/icons-material"
import { Box, Button, Typography } from "@mui/material"
import CreateDeviceDialog from "./CreateDeviceDialog"

const TwoFactorHeader: React.FC = () => {
  const [open, setOpen] = useState(false)

  const handleOpen = () => setOpen(true)
  const handleClose = () => setOpen(false)

  return (
    <Box sx={{ display: "flex", mb: 3 }}>
      <Typography variant="h5" sx={{ flexGrow: 1 }}>
        2FA Keys
      </Typography>
      <Box>
        <Button variant="outlined" startIcon={<Add />} onClick={handleOpen}>
          Add 2FA Key
        </Button>
      </Box>
      <CreateDeviceDialog open={open} onClose={handleClose} />
    </Box>
  )
}
export default TwoFactorHeader
