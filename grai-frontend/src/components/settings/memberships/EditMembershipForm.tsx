import React, { useState } from "react"
import { LoadingButton } from "@mui/lab"
import {
  Box,
  Checkbox,
  FormControlLabel,
  FormGroup,
  ListItemText,
  MenuItem,
  TextField,
} from "@mui/material"
import Form from "components/form/Form"

export type Values = {
  role: string
  is_active: boolean
}

export interface Membership {
  id: string
  role: string
  is_active: boolean
  user: {
    first_name: string | null
    last_name: string | null
    username: string | null
  }
}

type EditMembershipFormProps = {
  membership: Membership
  onSubmit: (values: Values) => void
  loading?: boolean
}

const EditMembershipForm: React.FC<EditMembershipFormProps> = ({
  membership,
  onSubmit,
  loading,
}) => {
  const [values, setValues] = useState<Values>(membership)

  const handleSubmit = () => onSubmit(values)

  return (
    <Form onSubmit={handleSubmit}>
      <TextField
        disabled
        value={membership.user.username}
        fullWidth
        required
        margin="normal"
      />
      <TextField
        select
        value={values.role}
        onChange={event => setValues({ ...values, role: event.target.value })}
        fullWidth
        required
        margin="normal"
        disabled={loading}
        inputProps={{ "data-testid": "role-select" }}
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
      <FormGroup sx={{ pl: 1 }}>
        <FormControlLabel
          control={
            <Checkbox
              checked={values.is_active}
              onChange={event =>
                setValues({ ...values, is_active: event.target.checked })
              }
            />
          }
          label="Active"
        />
      </FormGroup>
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

export default EditMembershipForm
