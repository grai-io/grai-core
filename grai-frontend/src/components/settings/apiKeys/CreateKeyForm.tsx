import { LoadingButton } from "@mui/lab"
import { TextField } from "@mui/material"
import React, { useState } from "react"
import Form from "../../form/Form"

export type Values = {
  name: string
}

type CreateKeyFormProps = {
  onSubmit: (values: Values) => void
  loading?: boolean
}

const CreateKeyForm: React.FC<CreateKeyFormProps> = ({ onSubmit, loading }) => {
  const [values, setValues] = useState<Values>({
    name: "",
  })

  const handleSubmit = () => onSubmit(values)

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
