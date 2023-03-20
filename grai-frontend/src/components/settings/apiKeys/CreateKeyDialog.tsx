import React, { useState } from "react"
import { gql, useMutation } from "@apollo/client"
import {
  Alert,
  AlertTitle,
  Dialog,
  DialogContent,
  Typography,
} from "@mui/material"
import { DateTime } from "luxon"
import DialogTitle from "components/dialogs/DialogTitle"
import CopyButton from "components/utils/CopyButton"
import GraphError from "components/utils/GraphError"
import {
  CreateApiKey,
  CreateApiKeyVariables,
} from "./__generated__/CreateApiKey"
import { NewApiKey } from "./__generated__/NewApiKey"
import CreateKeyForm from "./forms/CreateKeyForm"
import { ExpiryDate } from "./forms/ExpirationField"

export const CREATE_API_KEY = gql`
  mutation CreateApiKey(
    $workspaceId: ID!
    $name: String!
    $expiry_date: DateTime
  ) {
    createApiKey(
      workspaceId: $workspaceId
      name: $name
      expiry_date: $expiry_date
    ) {
      key
      api_key {
        id
        name
        expiry_date
        revoked
      }
    }
  }
`

export type Values = {
  name: string
  expiry_date: ExpiryDate
}

const defaultValues = {
  name: "",
  expiry_date: 30,
}

const expiryDateToString = (
  expiry_date: Values["expiry_date"]
): string | null => {
  if (!expiry_date || expiry_date === "none" || expiry_date === "custom")
    return null

  if (typeof expiry_date === "number")
    return DateTime.local().plus({ days: expiry_date }).toISO()

  return expiry_date.toISO()
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
  const [values, setValues] = useState<Values>(defaultValues)

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
        name: values.name,
        expiry_date: expiryDateToString(values.expiry_date),
        workspaceId,
      },
    })
      .then(res => res.data)
      .then(data => setKey(data?.createApiKey.key))
      .catch(err => {})

  const handleClose = () => {
    setValues(defaultValues)
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
