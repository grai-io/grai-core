import React, { useState } from "react"
import { Add } from "@mui/icons-material"
import { Box, Button, Typography } from "@mui/material"
import CreateMembershipDialog from "./CreateMembershipDialog"

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
    <Box sx={{ display: "flex", mb: 3 }}>
      <Typography variant="h5" sx={{ flexGrow: 1 }}>
        Memberships
      </Typography>
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
    </Box>
  )
}
export default MembershipsHeader
