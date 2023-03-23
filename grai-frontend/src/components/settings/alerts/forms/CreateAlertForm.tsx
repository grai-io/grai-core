import React, { useState } from "react"
import { LoadingButton } from "@mui/lab"
import { Box, TextField } from "@mui/material"
import Form from "components/form/Form"
import Channel from "./Channel"
import EmailChannel from "./EmailChannel"
import TriggersField, { Triggers } from "./Triggers"

export type Values = {
  name: string
  channel: string
  channel_metadata: any
  triggers: Triggers
}

type CreateAlertFormProps = {
  onSubmit: (values: Values) => void
  loading?: boolean
}

const CreateAlertForm: React.FC<CreateAlertFormProps> = ({
  onSubmit,
  loading,
}) => {
  const [values, setValues] = useState<Values>({
    name: "",
    channel: "",
    channel_metadata: {},
    triggers: {},
  })

  const handleSubmit = () => onSubmit(values)

  return (
    <Form onSubmit={handleSubmit}>
      <TextField
        label="Name"
        value={values.name}
        onChange={event => setValues({ ...values, name: event.target.value })}
        margin="normal"
        fullWidth
        required
      />
      <Channel
        value={values.channel}
        onChange={channel => setValues({ ...values, channel })}
      />
      {values.channel === "email" && (
        <EmailChannel
          value={values.channel_metadata}
          onChange={channel_metadata =>
            setValues({ ...values, channel_metadata })
          }
        />
      )}
      <TriggersField
        value={values.triggers}
        onChange={triggers => setValues({ ...values, triggers })}
      />
      <Box sx={{ textAlign: "right" }}>
        <LoadingButton
          variant="contained"
          type="submit"
          sx={{ mt: 2, color: "white", minWidth: 80 }}
          loading={loading}
        >
          Save
        </LoadingButton>
      </Box>
    </Form>
  )
}

export default CreateAlertForm
