import React from "react"
import { Dialog, styled } from "@mui/material"
import SearchContainer from "./SearchContainer"

const StyledDialog = styled(Dialog)(() => ({
  "& .MuiDialog-container": {
    alignItems: "flex-start",
  },
}))

type SearchDialogProps = {
  open: boolean
  onClose: () => void
  workspaceId: string
}

const SearchDialog: React.FC<SearchDialogProps> = ({
  open,
  onClose,
  workspaceId,
}) => {
  return (
    <StyledDialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      {open && <SearchContainer onClose={onClose} workspaceId={workspaceId} />}
    </StyledDialog>
  )
}

export default SearchDialog
