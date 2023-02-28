import React, { useState } from "react"
import { gql, useMutation } from "@apollo/client"
import { LoadingButton } from "@mui/lab"
import { Alert, Box, TextField, Typography } from "@mui/material"
import Form from "components/form/Form"
import GraphError from "components/utils/GraphError"
import {
  RequestPasswordReset,
  RequestPasswordResetVariables,
} from "./__generated__/RequestPasswordReset"

export const REQUEST_PASSWORD_RESET = gql`
  mutation RequestPasswordReset($email: String!) {
    requestPasswordReset(email: $email) {
      success
    }
  }
`

const RequestPasswordResetForm: React.FC = () => {
  const [email, setEmail] = useState("")
  const [submitted, setSubmitted] = useState(false)

  const [requestPasswordReset, { loading, error }] = useMutation<
    RequestPasswordReset,
    RequestPasswordResetVariables
  >(REQUEST_PASSWORD_RESET)

  if (submitted)
    return (
      <Alert severity="success" sx={{ mb: 2 }}>
        <Typography>Password reset email sent</Typography>
      </Alert>
    )

  const handleSubmit = () =>
    requestPasswordReset({
      variables: {
        email,
      },
    })
      .then(() => setSubmitted(true))
      .catch(err => {})

  return (
    <Box sx={{ pb: 2 }}>
      <Typography variant="h6">
        Enter your email to reset your password
      </Typography>
      <Form onSubmit={handleSubmit}>
        {error && <GraphError error={error} />}
        <TextField
          id="email"
          label="Email"
          type="email"
          fullWidth
          margin="normal"
          required
          value={email}
          disabled={loading}
          onChange={event => setEmail(event.target.value)}
        />
        <LoadingButton
          variant="contained"
          fullWidth
          type="submit"
          size="large"
          loading={loading}
          sx={{ height: 56, mt: 2 }}
        >
          SUBMIT
        </LoadingButton>
      </Form>
    </Box>
  )
}

export default RequestPasswordResetForm
