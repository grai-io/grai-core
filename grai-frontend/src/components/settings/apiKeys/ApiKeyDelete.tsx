import React from "react"
import { gql, useMutation } from "@apollo/client"
import { Delete } from "@mui/icons-material"
import { MenuItem, ListItemIcon, ListItemText } from "@mui/material"
import { useConfirm } from "material-ui-confirm"
import { useSnackbar } from "notistack"
import {
  DeleteApiKey,
  DeleteApiKeyVariables,
} from "./__generated__/DeleteApiKey"
import { ApiKey } from "./ApiKeyMenu"

export const DELETE_API_KEY = gql`
  mutation DeleteApiKey($id: ID!) {
    deleteApiKey(id: $id) {
      id
    }
  }
`

type ApiKeyDeleteProps = {
  apiKey: ApiKey
  onClose: () => void
  workspaceId?: string
}

const ApiKeyDelete: React.FC<ApiKeyDeleteProps> = ({
  apiKey,
  onClose,
  workspaceId,
}) => {
  const confirm = useConfirm()
  const { enqueueSnackbar } = useSnackbar()

  /* istanbul ignore next */
  const [deleteApiKey] = useMutation<DeleteApiKey, DeleteApiKeyVariables>(
    DELETE_API_KEY,
    {
      variables: { id: apiKey.id },
      update(cache, { data }) {
        cache.modify({
          id: cache.identify({
            id: workspaceId,
            __typename: "Workspace",
          }),
          fields: {
            api_keys(existingApiKeys = { data: [] }, { readField }) {
              if (!data?.deleteApiKey) return

              return {
                data: existingApiKeys.data.filter(
                  (keyRef: any) =>
                    data.deleteApiKey.id !== readField("id", keyRef)
                ),
              }
            },
          },
        })
      },
    }
  )

  const handleDelete = () => {
    onClose()
    confirm({
      title: "Delete API Key",
      description: `Are you sure you wish to delete the ${apiKey.name} key?`,
      confirmationText: "Delete",
    })
      .then(() => deleteApiKey())
      .then(() => enqueueSnackbar("API Key deleted", { variant: "success" }))
      .catch(error =>
        enqueueSnackbar(`Failed to delete API key ${error}`, {
          variant: "error",
        })
      )
  }

  return (
    <MenuItem onClick={handleDelete}>
      <ListItemIcon>
        <Delete />
      </ListItemIcon>
      <ListItemText primary="Delete" />
    </MenuItem>
  )
}

export default ApiKeyDelete
