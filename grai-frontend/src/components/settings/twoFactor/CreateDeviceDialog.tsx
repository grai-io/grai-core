import React from "react"
import { Dialog } from "@mui/material"
import DialogTitle from "components/dialogs/DialogTitle"
import CreateDeviceForm from "./CreateDeviceForm"

type CreateDeviceDialogProps = {
  open: boolean
  onClose: () => void
}

const CreateDeviceDialog: React.FC<CreateDeviceDialogProps> = ({
  open,
  onClose,
}) => (
  <Dialog open={open} onClose={onClose}>
    <DialogTitle onClose={onClose}>Add 2FA Device</DialogTitle>
    <CreateDeviceForm onClose={onClose} />
  </Dialog>
)

export default CreateDeviceDialog
