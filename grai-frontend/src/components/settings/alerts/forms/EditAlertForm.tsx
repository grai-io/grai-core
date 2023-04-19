import React, { useState } from "react"
import { ApolloError } from "@apollo/client"
import { LoadingButton } from "@mui/lab"
import { TextField } from "@mui/material"
import Form from "components/form/Form"
import GraphError from "components/utils/GraphError"
import EmailChannel from "./EmailChannel"
import TriggersField, { Triggers } from "./Triggers"

export interface Alert {
  name: string
  channel: string
  channel_metadata: any
  triggers: Triggers
}

export type Values = {
  name: string
  channel_metadata: any
  triggers: Triggers
}

type EditAlertFormProps = {
  alert: Alert
  onSubmit: (values: Values) => void
  error?: ApolloError
  loading?: boolean
}

const EditAlertForm: React.FC<EditAlertFormProps> = ({
  alert,
  onSubmit,
  error,
  loading,
}) => {
  const [values, setValues] = useState<Values>({
    name: alert.name,
    channel_metadata: alert.channel_metadata,
    triggers: alert.triggers,
  })

  const handleSubmit = () => onSubmit(values)

  return (
    <Form onSubmit={handleSubmit}>
      {error && <GraphError error={error} />}
      <TextField
        label="Name"
        value={values.name}
        onChange={event => setValues({ ...values, name: event.target.value })}
        disabled={loading}
        fullWidth
        required
        margin="normal"
      />
      {alert.channel === "email" && (
        <EmailChannel
          value={values.channel_metadata}
          onChange={channel_metadata =>
            setValues({ ...values, channel_metadata })
          }
          disabled={loading}
        />
      )}
      <TriggersField
        value={values.triggers}
        onChange={triggers => setValues({ ...values, triggers })}
        disabled={loading}
      />
      <LoadingButton
        type="submit"
        variant="contained"
        loading={loading}
        sx={{ mt: 2, minWidth: 80 }}
      >
        Save
      </LoadingButton>
    </Form>
  )
}

export default EditAlertForm
