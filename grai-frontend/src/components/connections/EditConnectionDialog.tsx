import { Dialog, DialogContent } from "@mui/material"
import DialogTitle from "components/dialogs/DialogTitle"
import React from "react"
import UpdateConnectionForm, { Connection } from "./UpdateConnectionForm"

type EditConnectionDialogProps = {
  open: boolean
  onClose: () => void
  connection: Connection
}

const EditConnectionDialog: React.FC<EditConnectionDialogProps> = ({
  open,
  onClose,
  connection,
}) => (
  <Dialog open={open} onClose={onClose}>
    <DialogTitle onClose={onClose}>Edit Connection</DialogTitle>
    <DialogContent>
      <UpdateConnectionForm connection={connection} onClose={onClose} />
    </DialogContent>
  </Dialog>
)

export default EditConnectionDialog
