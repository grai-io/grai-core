import { gql, useMutation } from "@apollo/client"
import {
  Alert,
  AlertTitle,
  Dialog,
  DialogContent,
  Typography,
} from "@mui/material"
import React, { useState } from "react"
import { useParams } from "react-router-dom"
import DialogTitle from "components/dialogs/DialogTitle"
import CopyButton from "components/utils/CopyButton"
import CreateKeyForm, { Values } from "./CreateKeyForm"
import {
  CreateApiKey,
  CreateApiKeyVariables,
} from "./__generated__/CreateApiKey"
import GraphError from "components/utils/GraphError"
import { onError } from "@apollo/client/link/error"

export const CREATE_API_KEY = gql`
  mutation CreateApiKey($name: String!, $workspaceId: ID!) {
    createApiKey(name: $name, workspaceId: $workspaceId) {
      key
      apiKey {
        id
        name
      }
    }
  }
`

type CreateKeyDialogProps = {
  open: boolean
  onClose: () => void
}

const CreateKeyDialog: React.FC<CreateKeyDialogProps> = ({ open, onClose }) => {
  const { workspaceId } = useParams()
  const [key, setKey] = useState<string>()

  const [createApiKey, { loading, error }] = useMutation<
    CreateApiKey,
    CreateApiKeyVariables
  >(CREATE_API_KEY)

  const handleSubmit = (values: Values) =>
    createApiKey({
      variables: {
        ...values,
        workspaceId: workspaceId ?? "",
      },
    })
      .then(res => res.data)
      .then(data => setKey(data?.createApiKey.key))
      .catch(err => {})

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle onClose={onClose}>Create API Key</DialogTitle>
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
          <CreateKeyForm onSubmit={handleSubmit} loading={loading} />
        )}
      </DialogContent>
    </Dialog>
  )
}

export default CreateKeyDialog
