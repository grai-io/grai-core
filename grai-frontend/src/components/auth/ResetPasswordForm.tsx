import React, { useState } from "react"
import { gql, useMutation } from "@apollo/client"
import { LoadingButton } from "@mui/lab"
import { Alert, Box, TextField, Typography } from "@mui/material"
import { useLocation } from "react-router-dom"
import Form from "components/form/Form"
import GraphError from "components/utils/GraphError"
import {
  ResetPassword,
  ResetPasswordVariables,
} from "./__generated__/ResetPassword"

export const RESET_PASSWORD = gql`
  mutation ResetPassword($token: String!, $uid: String!, $password: String!) {
    resetPassword(token: $token, uid: $uid, password: $password) {
      id
    }
  }
`

const ResetPasswordForm: React.FC = () => {
  const searchParams = new URLSearchParams(useLocation().search)

  const [password, setPassword] = useState("")
  const [submitted, setSubmitted] = useState(false)

  const [resetPassword, { loading, error }] = useMutation<
    ResetPassword,
    ResetPasswordVariables
  >(RESET_PASSWORD)

  if (submitted)
    return (
      <Alert severity="success" sx={{ mb: 2 }}>
        <Typography>Password reset, please login</Typography>
      </Alert>
    )

  const token = searchParams.get("token")
  const uid = searchParams.get("uid")

  if (!token || !uid)
    return <Alert severity="error">Missing required token</Alert>

  const handleSubmit = () =>
    resetPassword({
      variables: {
        token,
        uid,
        password,
      },
    })
      .then(() => setSubmitted(true))
      .catch(err => {})

  return (
    <Box sx={{ pb: 2 }}>
      <Typography variant="h6" sx={{ mb: 1 }}>
        Choose a new password
      </Typography>
      <Form onSubmit={handleSubmit}>
        {error && <GraphError error={error} />}
        <TextField
          label="Password"
          type="password"
          fullWidth
          margin="normal"
          required
          value={password}
          disabled={loading}
          onChange={event => setPassword(event.target.value)}
          inputProps={{
            "data-testid": "password",
          }}
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

export default ResetPasswordForm
