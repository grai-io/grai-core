import React from "react"
import { LoadingButton } from "@mui/lab"
import { Box, TextField } from "@mui/material"
import Form from "components/form/Form"
import ExpirationField from "./ExpirationField"
import { Values } from "../CreateKeyDialog"

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
      <ExpirationField
        value={values.expiry_date}
        onChange={value => setValues({ ...values, expiry_date: value })}
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

export default CreateKeyForm
