import React, { useState } from "react"
import { LoadingButton } from "@mui/lab"
import { TextField } from "@mui/material"
import Form from "components/form/Form"

export type Values = {
  name: string
}

type CreateFilterFormProps = {
  loading?: boolean
  onSubmit: (values: Values) => void
}

const CreateFilterForm: React.FC<CreateFilterFormProps> = ({
  loading,
  onSubmit,
}) => {
  const [values, setValues] = useState<Values>({
    name: "",
  })

  const handleSubmit = () => onSubmit(values)

  return (
    <Form onSubmit={handleSubmit}>
      <TextField
        label="Name"
        value={values.name}
        onChange={e => setValues({ ...values, name: e.target.value })}
        fullWidth
        required
        margin="normal"
      />
      <LoadingButton
        loading={loading}
        type="submit"
        variant="contained"
        fullWidth
        sx={{ mt: 2, height: 56 }}
      >
        Save
      </LoadingButton>
    </Form>
  )
}

export default CreateFilterForm
