import React, { useState } from "react"
import { LoadingButton } from "@mui/lab"
import { Box } from "@mui/material"
import MultipleEmails from "components/form/fields/MultipleEmails"
import Form from "components/form/Form"
import MembershipRole from "./MembershipRole"

export type Values = {
  role: string
  emails: string[]
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
    emails: [],
  })

  const handleSubmit = () => onSubmit(values)

  return (
    <Form onSubmit={handleSubmit}>
      <MultipleEmails
        value={values.emails}
        onChange={emails => setValues({ ...values, emails })}
      />
      <MembershipRole
        required
        disabled={loading}
        value={values.role}
        onChange={role => setValues({ ...values, role })}
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

export default CreateMembershipForm
