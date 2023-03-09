import React from "react"
import { MoreHoriz, Edit, DeleteOutline } from "@mui/icons-material"
import {
  IconButton,
  Menu,
  MenuItem,
  ListItemIcon,
  ListItemText,
} from "@mui/material"
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
          <MenuItem disabled>
            <ListItemIcon>
              <Edit />
            </ListItemIcon>
            <ListItemText primary="Edit" />
          </MenuItem>
          <MenuItem disabled>
            <ListItemIcon>
              <DeleteOutline />
            </ListItemIcon>
            <ListItemText primary="Revoke" />
          </MenuItem>
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
