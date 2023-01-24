import { Add } from "@mui/icons-material"
import { Box, Button, Typography } from "@mui/material"
import React, { useState } from "react"
import CreateKeyDialog from "./CreateKeyDialog"

type ApiKeysHeaderProps = {
  workspaceId: string
}

const ApiKeysHeader: React.FC<ApiKeysHeaderProps> = ({ workspaceId }) => {
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
      <CreateKeyDialog
        workspaceId={workspaceId}
        open={open}
        onClose={handleClose}
      />
    </Box>
  )
}
export default ApiKeysHeader
