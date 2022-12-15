import { LoadingButton } from "@mui/lab"
import { TextField, Typography } from "@mui/material"
import React, { useState } from "react"
import Connector, { ConnectorType } from "components/form/fields/Connector"
import Namespace from "components/form/fields/Namespace"
import Form from "components/form/Form"
import ConnectionsMetadata from "./ConnectionsMetadata"

export type Values = {
  connector: ConnectorType | null
  namespace: string | null
  name: string
  metadata: any
  secrets: any
}

type ConnectionsFormProps = {
  defaultValues: Values
  onSubmit: (values: Values) => void
  error?: any
  loading?: boolean
  edit?: boolean
}

const ConnectionsForm: React.FC<ConnectionsFormProps> = ({
  defaultValues,
  onSubmit,
  error,
  loading,
  edit,
}) => {
  const [values, setValues] = useState<Values>(defaultValues)

  const handleSubmit = () => onSubmit(values)

  return (
    <Form onSubmit={handleSubmit}>
      {error && <Typography>{JSON.stringify(error)}</Typography>}
      {!edit && (
        <Connector
          value={values.connector}
          onChange={value => setValues({ ...values, connector: value })}
        />
      )}

      <Namespace
        value={values.namespace}
        onChange={value => setValues({ ...values, namespace: value })}
      />
      <TextField
        label="Name"
        margin="normal"
        value={values.name}
        onChange={event => setValues({ ...values, name: event.target.value })}
        required
        fullWidth
      />
      {values.connector && (
        <ConnectionsMetadata
          connector={values.connector}
          metadata={values.metadata}
          secrets={values.secrets}
          onChangeMetadata={value => setValues({ ...values, metadata: value })}
          onChangeSecrets={value => setValues({ ...values, secrets: value })}
          edit={edit}
        />
      )}
      <LoadingButton
        variant="contained"
        type="submit"
        sx={{ mt: 2 }}
        loading={loading}
      >
        Save
      </LoadingButton>
    </Form>
  )
}

export default ConnectionsForm
