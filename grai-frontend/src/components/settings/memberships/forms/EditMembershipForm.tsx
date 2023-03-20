import React, { useState } from "react"
import { LoadingButton } from "@mui/lab"
import {
  Box,
  Checkbox,
  FormControlLabel,
  FormGroup,
  TextField,
} from "@mui/material"
import Form from "components/form/Form"
import MembershipRole from "./MembershipRole"

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
      <MembershipRole
        required
        disabled={loading}
        value={values.role}
        onChange={role => setValues({ ...values, role })}
      />
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
