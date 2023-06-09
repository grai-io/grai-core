import React from "react"
import { MoreHoriz } from "@mui/icons-material"
import { IconButton, Menu } from "@mui/material"
import PopupState, { bindMenu, bindTrigger } from "material-ui-popup-state"
import useWorkspace from "helpers/useWorkspace"
import ConnectionDelete, { Connection } from "./ConnectionDelete"

type ConnectionMenuProps = {
  connection: Connection
  workspaceId: string
}

const ConnectionMenu: React.FC<ConnectionMenuProps> = ({
  connection,
  workspaceId,
}) => {
  const { workspaceNavigate } = useWorkspace()

  const handleDelete = () => workspaceNavigate("connections")

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
            <ConnectionDelete
              connection={connection}
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

export default ConnectionMenu
