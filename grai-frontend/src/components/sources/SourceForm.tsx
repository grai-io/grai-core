import React, { useState } from "react"
import { ApolloError } from "@apollo/client"
import { LoadingButton } from "@mui/lab"
import { TextField } from "@mui/material"
import Form from "components/form/Form"
import GraphError from "components/utils/GraphError"

export type Values = {
  name: string
  priority: number
}

type SourceFormProps = {
  defaultValues: Values
  onSubmit: (values: Values) => void
  loading?: boolean
  error?: ApolloError
}

const SourceForm: React.FC<SourceFormProps> = ({
  defaultValues,
  onSubmit,
  loading,
  error,
}) => {
  const [values, setValues] = useState<Values>(defaultValues)

  const handleSubmit = () => onSubmit(values)

  return (
    <Form onSubmit={handleSubmit}>
      {error && <GraphError error={error} />}
      <TextField
        label="Name"
        value={values.name}
        onChange={event => setValues({ ...values, name: event.target.value })}
        margin="normal"
        required
        fullWidth
      />
      <TextField
        label="Priority"
        value={values.priority}
        onChange={event =>
          setValues({ ...values, priority: parseInt(event.target.value) })
        }
        margin="normal"
        type="number"
        required
        fullWidth
      />
      <LoadingButton
        type="submit"
        loading={loading}
        variant="contained"
        sx={{ mt: 2 }}
      >
        Save
      </LoadingButton>
    </Form>
  )
}

export default SourceForm
