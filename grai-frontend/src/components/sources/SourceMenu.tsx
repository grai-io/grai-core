import React from "react"
import { MoreHoriz } from "@mui/icons-material"
import { IconButton, Menu } from "@mui/material"
import PopupState, { bindMenu, bindTrigger } from "material-ui-popup-state"
import useWorkspace from "helpers/useWorkspace"
import SourceDelete, { Source } from "./SourceDelete"

type SourceMenuProps = {
  source: Source
  workspaceId: string
}

const SourceMenu: React.FC<SourceMenuProps> = ({ source, workspaceId }) => {
  const { workspaceNavigate } = useWorkspace()

  const handleDelete = () => workspaceNavigate("sources")

  return (
    <PopupState variant="popover">
      {popupState => (
        <>
          <IconButton size="small" {...bindTrigger(popupState)}>
            <MoreHoriz />
          </IconButton>

          <Menu
            {...bindMenu(popupState)}
            PaperProps={{
              sx: {
                width: 200,
              },
            }}
          >
            <SourceDelete
              source={source}
              onClose={popupState.close}
              onDelete={handleDelete}
              workspaceId={workspaceId}
            />
          </Menu>
        </>
      )}
    </PopupState>
  )
}

export default SourceMenu
