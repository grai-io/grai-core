import React from "react"
import { MoreHoriz } from "@mui/icons-material"
import { IconButton, Menu } from "@mui/material"
import PopupState, { bindTrigger, bindMenu } from "material-ui-popup-state"
import ApiKeyDelete from "./ApiKeyDelete"

export interface ApiKey {
  id: string
  name: string
}

type ApiKeyMenuProps = {
  apiKey: ApiKey
  workspaceId?: string
}

const ApiKeyMenu: React.FC<ApiKeyMenuProps> = ({ apiKey, workspaceId }) => (
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
          <ApiKeyDelete
            apiKey={apiKey}
            onClose={popupState.close}
            workspaceId={workspaceId}
          />
        </Menu>
      </>
    )}
  </PopupState>
)

export default ApiKeyMenu
