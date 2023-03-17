import React, { useState } from "react"
import { LoadingButton } from "@mui/lab"
import { TextField } from "@mui/material"
import Form from "components/form/Form"
import GraphError from "components/utils/GraphError"
import ConnectionsMetadata from "./ConnectionsMetadata"

export interface ConnectorMetadataField {
  name: string
  label?: string
  secret?: boolean
  required?: boolean
  default?: string | number
  helper_text?: string | null
}

export interface ConnectorMetadata {
  docs_url?: string | null
  fields?: ConnectorMetadataField[]
  file?: {
    name?: string | null
    extension?: string | null
  } | null
}

export interface ConnectorType {
  id: string
  name: string
  metadata: ConnectorMetadata | null | undefined
  icon?: string | null
}

export type Values = {
  connector: ConnectorType | null
  namespace: string
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
      {error && <GraphError error={error} />}
      <TextField
        label="Namespace"
        margin="normal"
        value={values.namespace}
        onChange={event =>
          setValues({ ...values, namespace: event.target.value })
        }
        required
        fullWidth
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
