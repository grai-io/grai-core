import React, { useState } from "react"
import { Add } from "@mui/icons-material"
import { Box, Button } from "@mui/material"
import CreateMembershipDialog from "./CreateMembershipDialog"
import SettingsAppBar from "../SettingsAppBar"

type MembershipsHeaderProps = {
  workspaceId: string
}

const MembershipsHeader: React.FC<MembershipsHeaderProps> = ({
  workspaceId,
}) => {
  const [open, setOpen] = useState(false)

  const handleOpen = () => setOpen(true)
  const handleClose = () => setOpen(false)

  return (
    <SettingsAppBar
      title="Memberships"
      buttons={
        <>
          <Box>
            <Button variant="outlined" startIcon={<Add />} onClick={handleOpen}>
              Invite users
            </Button>
          </Box>
          <CreateMembershipDialog
            workspaceId={workspaceId}
            open={open}
            onClose={handleClose}
          />
        </>
      }
    />
  )
}
export default MembershipsHeader
