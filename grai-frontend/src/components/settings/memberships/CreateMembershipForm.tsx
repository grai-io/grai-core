import React, { useState } from "react"
import { LoadingButton } from "@mui/lab"
import { Box, ListItemText, MenuItem, TextField } from "@mui/material"
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
    role: "member",
    email: "",
  })

  const handleSubmit = () => onSubmit(values)

  return (
    <Form onSubmit={handleSubmit}>
      <TextField
        value={values.email}
        onChange={event => setValues({ ...values, email: event.target.value })}
        fullWidth
        required
        margin="normal"
        disabled={loading}
        placeholder="Enter emails"
      />
      <TextField
        select
        value={values.role}
        onChange={event => setValues({ ...values, role: event.target.value })}
        fullWidth
        required
        margin="normal"
        disabled={loading}
      >
        <MenuItem value="admin">
          <ListItemText
            primary="Admin"
            secondary="Can add and remove members"
          />
        </MenuItem>
        <MenuItem value="member">
          <ListItemText
            primary="Member"
            secondary="Can edit but not add or remove members"
          />
        </MenuItem>
        <MenuItem value="read_only">
          <ListItemText primary="Read Only" secondary="Can only view data" />
        </MenuItem>
      </TextField>
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

export default CreateMembershipForm
