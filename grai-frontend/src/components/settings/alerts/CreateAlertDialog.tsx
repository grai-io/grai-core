import React from "react"
import { gql, useMutation } from "@apollo/client"
import { Dialog, DialogContent } from "@mui/material"
import { useSnackbar } from "notistack"
import DialogTitle from "components/dialogs/DialogTitle"
import GraphError from "components/utils/GraphError"
import { CreateAlert, CreateAlertVariables } from "./__generated__/CreateAlert"
import { NewAlert } from "./__generated__/NewAlert"
import CreateAlertForm, { Values } from "./forms/CreateAlertForm"

export const CREATE_ALERT = gql`
  mutation CreateAlert(
    $workspaceId: ID!
    $name: String!
    $channel: String!
    $channel_metadata: JSON!
    $triggers: JSON!
  ) {
    createAlert(
      workspaceId: $workspaceId
      name: $name
      channel: $channel
      channel_metadata: $channel_metadata
      triggers: $triggers
    ) {
      id
      name
      channel
      channel_metadata
      triggers
      is_active
      created_at
    }
  }
`

type CreateAlertDialogProps = {
  workspaceId: string
  open: boolean
  onClose: () => void
}

const CreateAlertDialog: React.FC<CreateAlertDialogProps> = ({
  workspaceId,
  open,
  onClose,
}) => {
  const { enqueueSnackbar } = useSnackbar()

  const [createAlert, { loading, error }] = useMutation<
    CreateAlert,
    CreateAlertVariables
  >(CREATE_ALERT, {
    update(cache, { data }) {
      cache.modify({
        id: cache.identify({
          id: workspaceId,
          __typename: "Workspace",
        }),
        fields: {
          /* istanbul ignore next */
          alerts(existingApiKeys = { data: [] }) {
            if (!data?.createAlert) return existingApiKeys

            const newApiKey = cache.writeFragment<NewAlert>({
              data: data.createAlert,
              fragment: gql`
                fragment NewAlert on Alert {
                  id
                  name
                  channel
                  channel_metadata
                  triggers
                  is_active
                  created_at
                }
              `,
            })
            return { data: [...existingApiKeys.data, newApiKey] }
          },
        },
      })
    },
  })

  const handleSubmit = (values: Values) =>
    createAlert({
      variables: {
        ...values,
        workspaceId,
      },
    })
      .then(() => onClose())
      .then(() => enqueueSnackbar("Alert added"))
      .catch(err => {})

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="md">
      <DialogTitle onClose={onClose}>Add alert</DialogTitle>
      <DialogContent>
        {error && <GraphError error={error} />}
        <CreateAlertForm onSubmit={handleSubmit} loading={loading} />
      </DialogContent>
    </Dialog>
  )
}

export default CreateAlertDialog
