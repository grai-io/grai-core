import React, { useState } from "react"
import { gql, useMutation } from "@apollo/client"
import {
  Alert,
  AlertTitle,
  Dialog,
  DialogContent,
  Typography,
} from "@mui/material"
import DialogTitle from "components/dialogs/DialogTitle"
import CopyButton from "components/utils/CopyButton"
import GraphError from "components/utils/GraphError"
import {
  CreateApiKey,
  CreateApiKeyVariables,
} from "./__generated__/CreateApiKey"
import { NewApiKey } from "./__generated__/NewApiKey"
import CreateKeyForm from "./CreateKeyForm"

export const CREATE_API_KEY = gql`
  mutation CreateApiKey($name: String!, $workspaceId: ID!) {
    createApiKey(name: $name, workspaceId: $workspaceId) {
      key
      api_key {
        id
        name
      }
    }
  }
`

export type Values = {
  name: string
}

type CreateKeyDialogProps = {
  workspaceId: string
  open: boolean
  onClose: () => void
}

const CreateKeyDialog: React.FC<CreateKeyDialogProps> = ({
  workspaceId,
  open,
  onClose,
}) => {
  const [key, setKey] = useState<string>()
  const [values, setValues] = useState<Values>({
    name: "",
  })

  const [createApiKey, { loading, error }] = useMutation<
    CreateApiKey,
    CreateApiKeyVariables
  >(CREATE_API_KEY, {
    update(cache, { data }) {
      cache.modify({
        id: cache.identify({
          id: workspaceId,
          __typename: "Workspace",
        }),
        fields: {
          api_keys(existingApiKeys = []) {
            if (!data?.createApiKey) return

            const newApiKey = cache.writeFragment<NewApiKey>({
              data: data.createApiKey.api_key,
              fragment: gql`
                fragment NewApiKey on WorkspaceAPIKey {
                  id
                  name
                }
              `,
            })
            return [...existingApiKeys, newApiKey]
          },
        },
      })
    },
  })

  const handleSubmit = () =>
    createApiKey({
      variables: {
        ...values,
        workspaceId,
      },
    })
      .then(res => res.data)
      .then(data => setKey(data?.createApiKey.key))
      .catch(err => {})

  const handleClose = () => {
    setValues({
      name: "",
    })
    setKey(undefined)
    onClose()
  }

  return (
    <Dialog open={open} onClose={handleClose} fullWidth maxWidth="sm">
      <DialogTitle onClose={handleClose}>Create API Key</DialogTitle>
      <DialogContent>
        {error && <GraphError error={error} />}
        {key ? (
          <Alert severity="success">
            <AlertTitle>API key created</AlertTitle>
            <Typography sx={{ my: 1 }} variant="body2">
              {key}
              <CopyButton text={key} />
            </Typography>
            Please store it somewhere safe as you will not be able to see it
            again.
          </Alert>
        ) : (
          <CreateKeyForm
            onSubmit={handleSubmit}
            loading={loading}
            values={values}
            setValues={setValues}
          />
        )}
      </DialogContent>
    </Dialog>
  )
}

export default CreateKeyDialog
