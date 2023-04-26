import React from "react"
import { Box, Dialog } from "@mui/material"
import DialogTitle from "components/dialogs/DialogTitle"
import FilterForm from "./FilterForm"

type FilterDialogProps = {
  open: boolean
  onClose: () => void
}

const FilterDialog: React.FC<FilterDialogProps> = ({ open, onClose }) => {
  return (
    <Dialog open={open} onClose={onClose} maxWidth="lg" fullWidth>
      <DialogTitle onClose={onClose}>Filter</DialogTitle>
      <Box sx={{ p: 3, pt: 1 }}>
        <FilterForm onClose={onClose} />
      </Box>
    </Dialog>
  )
}

export default FilterDialog
