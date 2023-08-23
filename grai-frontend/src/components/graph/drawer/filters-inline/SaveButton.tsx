import React, { useState } from "react"
import { Save } from "@mui/icons-material"
import { Button } from "@mui/material"
import { Filter } from "components/filters/filters"
import SaveDialog from "./SaveDialog"

type SaveButtonProps = {
  workspaceId: string
  inlineFilters: Filter[]
}

const SaveButton: React.FC<SaveButtonProps> = ({
  workspaceId,
  inlineFilters,
}) => {
  const [open, setOpen] = useState(false)

  const handleOpen = () => setOpen(true)
  const handleClose = () => setOpen(false)

  return (
    <>
      <Button
        variant="outlined"
        fullWidth
        startIcon={<Save />}
        sx={{ mb: 1 }}
        onClick={handleOpen}
      >
        Save
      </Button>
      <SaveDialog
        open={open}
        onClose={handleClose}
        workspaceId={workspaceId}
        inlineFilters={inlineFilters}
      />
    </>
  )
}

export default SaveButton
