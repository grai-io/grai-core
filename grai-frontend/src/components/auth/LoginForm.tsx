import React, { useState } from "react"
import { gql, useMutation } from "@apollo/client"
import { LoadingButton } from "@mui/lab"
import { Box, TextField } from "@mui/material"
import posthog from "posthog"
import { Link } from "react-router-dom"
import Form from "components/form/Form"
import GraphError from "components/utils/GraphError"
import { Login, LoginVariables } from "./__generated__/Login"
import useAuth from "./useAuth"

export const LOGIN = gql`
  mutation Login($username: String!, $password: String!) {
    login(username: $username, password: $password) {
      id
      username
      first_name
      last_name
    }
  }
`

type Values = {
  username: string
  password: string
}

const LoginForm: React.FC = () => {
  const { setLoggedIn } = useAuth()
  const [values, setValues] = useState<Values>({
    username: "",
    password: "",
  })

  const [login, { loading, error }] = useMutation<Login, LoginVariables>(LOGIN)

  const handleSubmit = () =>
    login({ variables: values })
      .then(data => data.data?.login)
      .then(user => user && posthog.identify(user.id, { email: user.username }))
      .then(() => setLoggedIn(true))
      .catch(() => {})

  return (
    <Box sx={{ pb: 2 }}>
      <Form onSubmit={handleSubmit}>
        {error && <GraphError error={error} />}
        <TextField
          id="email"
          label="Email"
          type="email"
          fullWidth
          margin="normal"
          required
          value={values.username}
          disabled={loading}
          onChange={event =>
            setValues({ ...values, username: event.target.value })
          }
        />
        <TextField
          inputProps={{ "data-testid": "password" }}
          label="Password"
          type="password"
          fullWidth
          margin="normal"
          required
          value={values.password}
          disabled={loading}
          error={!!error}
          onChange={event =>
            setValues({ ...values, password: event.target.value })
          }
        />
        <Box sx={{ m: 1 }}>
          <Link to="/forgot" style={{ textDecoration: "none", fontSize: 14 }}>
            Forgot your password?
          </Link>
        </Box>
        <LoadingButton
          variant="contained"
          fullWidth
          type="submit"
          size="large"
          loading={loading}
          sx={{ height: 56, mt: 2 }}
        >
          LOGIN
        </LoadingButton>
      </Form>
    </Box>
  )
}

export default LoginForm
