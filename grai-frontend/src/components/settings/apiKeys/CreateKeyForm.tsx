import React from "react"
import { LoadingButton } from "@mui/lab"
import { TextField } from "@mui/material"
import Form from "components/form/Form"
import { Values } from "./CreateKeyDialog"

type CreateKeyFormProps = {
  onSubmit: () => void
  loading?: boolean
  values: Values
  setValues: (values: Values) => void
}

const CreateKeyForm: React.FC<CreateKeyFormProps> = ({
  onSubmit,
  loading,
  values,
  setValues,
}) => {
  const handleSubmit = () => onSubmit()

  return (
    <Form onSubmit={handleSubmit}>
      <TextField
        label="Name"
        value={values.name}
        onChange={event => setValues({ ...values, name: event.target.value })}
        fullWidth
        required
        margin="normal"
        disabled={loading}
      />
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

export default CreateKeyForm
