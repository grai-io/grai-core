import React, { useState } from "react"
import { LoadingButton } from "@mui/lab"
import { TextField } from "@mui/material"
import Form from "components/form/Form"

export type Values = {
  role: string
  email: string
}

type CreateMembershipFormProps = {
  onSubmit: (values: Values) => void
  loading?: boolean
}

const CreateMembershipForm: React.FC<CreateMembershipFormProps> = ({
  onSubmit,
  loading,
}) => {
  const [values, setValues] = useState<Values>({
    role: "admin",
    email: "",
  })

  const handleSubmit = () => onSubmit(values)

  return (
    <Form onSubmit={handleSubmit}>
      <TextField
        label="Email"
        value={values.email}
        onChange={event => setValues({ ...values, email: event.target.value })}
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

export default CreateMembershipForm
