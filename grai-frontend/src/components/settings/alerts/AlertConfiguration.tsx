import React from "react"
import { gql, useMutation } from "@apollo/client"
import { useSnackbar } from "notistack"
import useWorkspace from "helpers/useWorkspace"
import { UpdateAlert, UpdateAlertVariables } from "./__generated__/UpdateAlert"
import EditAlertForm, {
  Alert as BaseAlert,
  Values,
} from "./forms/EditAlertForm"

export const UPDATE_ALERT = gql`
  mutation UpdateAlert(
    $id: ID!
    $name: String!
    $channel_metadata: JSON!
    $triggers: JSON!
    $is_active: Boolean!
  ) {
    updateAlert(
      id: $id
      name: $name
      channel_metadata: $channel_metadata
      triggers: $triggers
      is_active: $is_active
    ) {
      id
      name
      channel
      channel_metadata
      triggers
      is_active
    }
  }
`

interface Alert extends BaseAlert {
  id: string
}

type AlertConfigurationProps = {
  alert: Alert
}

const AlertConfiguration: React.FC<AlertConfigurationProps> = ({ alert }) => {
  const { enqueueSnackbar } = useSnackbar()
  const { workspaceNavigate } = useWorkspace()

  const [updateMembership, { loading, error }] = useMutation<
    UpdateAlert,
    UpdateAlertVariables
  >(UPDATE_ALERT)

  const handleSubmit = (values: Values) =>
    updateMembership({
      variables: {
        id: alert.id,
        name: values.name,
        channel_metadata: values.channel_metadata,
        triggers: values.triggers,
        is_active: true,
      },
    })
      .then(() => enqueueSnackbar("Membership updated"))
      .then(() => workspaceNavigate("settings/alerts/"))
      .catch(err => {})

  return (
    <EditAlertForm
      alert={alert}
      onSubmit={handleSubmit}
      error={error}
      loading={loading}
    />
  )
}

export default AlertConfiguration
