import React, { useState } from "react"
import { gql, useMutation } from "@apollo/client"
import { LoadingButton } from "@mui/lab"
import { InputLabel, TextField, styled } from "@mui/material"
import Form from "components/form/Form"
import GraphError from "components/utils/GraphError"
import posthog from "posthog"
import { Register, RegisterVariables } from "./__generated__/Register"
import useAuth from "../useAuth"

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

const StyledInputLabel = styled(InputLabel)(theme => ({
  fontWeight: 600,
  fontSize: 14,
  color: "#263238",
  marginTop: theme.theme.spacing(2),
  marginBottom: theme.theme.spacing(1),
}))

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
      <StyledInputLabel>Name</StyledInputLabel>
      <TextField
        fullWidth
        required
        placeholder="Insert your name"
        inputProps={{ "data-testid": "name" }}
        value={values.name}
        onChange={event => setValues({ ...values, name: event.target.value })}
        InputProps={{
          sx: { borderRadius: "8px" },
        }}
      />
      <StyledInputLabel>Email</StyledInputLabel>
      <TextField
        placeholder="yourname@mail.com"
        inputProps={{ "data-testid": "email" }}
        type="email"
        fullWidth
        required
        value={values.username}
        onChange={event =>
          setValues({ ...values, username: event.target.value })
        }
        InputProps={{
          sx: { borderRadius: "8px" },
        }}
      />
      <StyledInputLabel>Password</StyledInputLabel>
      <TextField
        placeholder="********"
        inputProps={{ "data-testid": "password" }}
        type="password"
        fullWidth
        required
        value={values.password}
        onChange={event =>
          setValues({ ...values, password: event.target.value })
        }
        InputProps={{
          sx: { borderRadius: "8px" },
        }}
      />
      <LoadingButton
        variant="contained"
        fullWidth
        type="submit"
        size="large"
        loading={loading}
        sx={{
          height: 56,
          my: 3,
          color: "white",
          backgroundColor: "#FC6016",
          fontSize: 18,
          fontWeight: 600,
          borderRadius: "8px",
          boxShadow: "0px 4px 6px #FC601620",
        }}
      >
        Get Started
      </LoadingButton>
    </Form>
  )
}

export default RegisterForm
