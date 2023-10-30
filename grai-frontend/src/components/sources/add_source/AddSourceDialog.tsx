import React from "react"
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Typography,
} from "@mui/material"
import { Link } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"

type AddSourceDialogProps = {
  open: boolean
  onClose: () => void
  organisationId: string
}

const AddSourceDialog: React.FC<AddSourceDialogProps> = ({
  open,
  onClose,
  organisationId,
}) => {
  const { routePrefix } = useWorkspace()

  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>Add Source</DialogTitle>
      <DialogContent>
        <Typography variant="body1" sx={{ mb: 1 }}>
          You are currently in a demo workspace.
        </Typography>
        <Typography variant="body1">
          We suggest you create a new workspace to add a source.
        </Typography>
      </DialogContent>
      <DialogActions>
        <Button component={Link} to={`${routePrefix}/connections/create`}>
          Add Source
        </Button>
        <Button
          component={Link}
          to={`/workspaces/create?organisationId=${organisationId}`}
        >
          Add Workspace
        </Button>
        <Button onClick={onClose}>Cancel</Button>
      </DialogActions>
    </Dialog>
  )
}

export default AddSourceDialog
