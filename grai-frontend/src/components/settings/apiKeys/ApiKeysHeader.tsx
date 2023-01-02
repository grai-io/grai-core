import { Add } from "@mui/icons-material"
import { Box, Button, Typography } from "@mui/material"
import React, { useState } from "react"
import CreateKeyDialog from "./CreateKeyDialog"

const ApiKeysHeader: React.FC = () => {
  const [open, setOpen] = useState(false)

  const handleOpen = () => setOpen(true)
  const handleClose = () => setOpen(false)

  return (
    <Box sx={{ display: "flex", mb: 3 }}>
      <Typography variant="h5" sx={{ flexGrow: 1 }}>
        API Keys
      </Typography>
      <Box>
        <Button variant="outlined" startIcon={<Add />} onClick={handleOpen}>
          Add API Key
        </Button>
      </Box>
      <CreateKeyDialog open={open} onClose={handleClose} />
    </Box>
  )
}
export default ApiKeysHeader
