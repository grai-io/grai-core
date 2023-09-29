import React, { useState } from "react"
import { Add } from "@mui/icons-material"
import { Box, Button, Card, Typography } from "@mui/material"
import CreateKeyDialog from "./CreateKeyDialog"
import SettingsAppBar from "../SettingsAppBar"

type ApiKeysHeaderProps = {
  workspaceId: string
}

const ApiKeysHeader: React.FC<ApiKeysHeaderProps> = ({ workspaceId }) => {
  const [open, setOpen] = useState(false)

  const handleOpen = () => setOpen(true)
  const handleClose = () => setOpen(false)

  return (
    <>
      <SettingsAppBar
        title="API Keys"
        buttons={
          <>
            <Box>
              <Button
                variant="outlined"
                startIcon={<Add />}
                onClick={handleOpen}
              >
                Add API Key
              </Button>
            </Box>
            <CreateKeyDialog
              workspaceId={workspaceId}
              open={open}
              onClose={handleClose}
            />
          </>
        }
      />
      <Box sx={{ p: 3, pb: 0 }}>
        <Card variant="outlined" sx={{ mt: 3, mb: 3, p: 2, display: "flex" }}>
          <Typography variant="body2" sx={{ mr: 2, mt: 0.25 }}>
            WorkspaceId
          </Typography>
          <Typography>{workspaceId}</Typography>
        </Card>
      </Box>
    </>
  )
}
export default ApiKeysHeader
