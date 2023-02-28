import React, { useState } from "react"
import { gql, useMutation } from "@apollo/client"
import { LoadingButton } from "@mui/lab"
import { TextField } from "@mui/material"
import posthog from "posthog"
import Form from "components/form/Form"
import GraphError from "components/utils/GraphError"
import { Register, RegisterVariables } from "./__generated__/Register"
import useAuth from "./useAuth"

export const REGISTER = gql`
  mutation Register($username: String!, $name: String!, $password: String!) {
    register(username: $username, name: $name, password: $password) {
      id
      username
      first_name
      last_name
    }
  }
`

type FormValues = {
  username: string
  name: string
  password: string
}

const RegisterForm: React.FC = () => {
  const { setLoggedIn } = useAuth()
  const [values, setValues] = useState<FormValues>({
    username: "",
    name: "",
    password: "",
  })

  const [register, { loading, error }] = useMutation<
    Register,
    RegisterVariables
  >(REGISTER)

  const handleSubmit = async () =>
    register({ variables: values })
      .then(data => data.data?.register)
      .then(user => user && posthog.identify(user.id, { email: user.username }))
      .then(() => setLoggedIn(true))
      .catch(() => {})

  return (
    <Form onSubmit={handleSubmit}>
      {error && <GraphError error={error} />}
      <TextField
        id="name"
        label="Name"
        fullWidth
        margin="normal"
        required
        value={values.name}
        onChange={event => setValues({ ...values, name: event.target.value })}
      />
      <TextField
        id="email"
        label="Email"
        type="email"
        fullWidth
        margin="normal"
        required
        value={values.username}
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
        onChange={event =>
          setValues({ ...values, password: event.target.value })
        }
      />
      <LoadingButton
        variant="contained"
        fullWidth
        type="submit"
        size="large"
        loading={loading}
        sx={{ height: 56, my: 2, color: "white" }}
      >
        REGISTER
      </LoadingButton>
    </Form>
  )
}

export default RegisterForm
