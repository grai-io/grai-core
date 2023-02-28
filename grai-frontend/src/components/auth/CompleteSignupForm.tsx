import React, { useState } from "react"
import { gql, useMutation } from "@apollo/client"
import { LoadingButton } from "@mui/lab"
import { Alert, Box, Button, TextField, Typography } from "@mui/material"
import { useLocation, Link } from "react-router-dom"
import Form from "components/form/Form"
import GraphError from "components/utils/GraphError"
import {
  CompleteSignup,
  CompleteSignupVariables,
} from "./__generated__/CompleteSignup"

export const COMPLETE_SIGNUP = gql`
  mutation CompleteSignup(
    $token: String!
    $uid: String!
    $first_name: String!
    $last_name: String!
    $password: String!
  ) {
    completeSignup(
      token: $token
      uid: $uid
      first_name: $first_name
      last_name: $last_name
      password: $password
    ) {
      id
    }
  }
`

type Values = {
  first_name: string
  last_name: string
  password: string
}

const CompleteSignupForm: React.FC = () => {
  const searchParams = new URLSearchParams(useLocation().search)

  const [values, setValues] = useState<Values>({
    first_name: "",
    last_name: "",
    password: "",
  })
  const [submitted, setSubmitted] = useState(false)

  const [completeSignup, { loading, error }] = useMutation<
    CompleteSignup,
    CompleteSignupVariables
  >(COMPLETE_SIGNUP)

  if (submitted)
    return (
      <>
        <Alert severity="success" sx={{ mb: 2 }}>
          <Typography>
            You are all signed up, please login to view your workspace.
          </Typography>
        </Alert>
        <Box sx={{ textAlign: "center" }}>
          <Button component={Link} to="/login" variant="outlined">
            Login
          </Button>
        </Box>
      </>
    )

  const token = searchParams.get("token")
  const uid = searchParams.get("uid")

  if (!token || !uid)
    return <Alert severity="error">Missing required token</Alert>

  const handleSubmit = () =>
    completeSignup({
      variables: {
        token,
        uid,
        ...values,
      },
    })
      .then(() => setSubmitted(true))
      .catch(err => {})

  return (
    <Box sx={{ pb: 2 }}>
      <Typography variant="h6" sx={{ mb: 2 }}>
        Welcome to Grai, let's get started
      </Typography>
      <Form onSubmit={handleSubmit}>
        {error && <GraphError error={error} />}
        <TextField
          label="First Name"
          fullWidth
          margin="normal"
          required
          value={values.first_name}
          disabled={loading}
          onChange={event =>
            setValues({ ...values, first_name: event.target.value })
          }
        />
        <TextField
          label="Last Name"
          fullWidth
          margin="normal"
          required
          value={values.last_name}
          disabled={loading}
          onChange={event =>
            setValues({ ...values, last_name: event.target.value })
          }
        />
        <TextField
          label="Password"
          type="password"
          fullWidth
          margin="normal"
          required
          value={values.password}
          disabled={loading}
          onChange={event =>
            setValues({ ...values, password: event.target.value })
          }
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

export default CompleteSignupForm
