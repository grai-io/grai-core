import React, { useState } from "react"
import { ApolloError } from "@apollo/client"
import { LoadingButton } from "@mui/lab"
import { TextField } from "@mui/material"
import Form from "components/form/Form"
import useAuth from "./useAuth"

type FormValues = {
  username: string
  name: string
  password: string
}

const RegisterForm: React.FC = () => {
  const { registerUser } = useAuth()
  const [values, setValues] = useState<FormValues>({
    username: "",
    name: "",
    password: "",
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<ApolloError>()

  const handleSubmit = async () => {
    setLoading(true)

    await registerUser(values).catch(err => {
      setError(err)
      setLoading(false)
    })
  }

  return (
    <Form onSubmit={handleSubmit}>
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
        error={!!error}
        helperText={error?.graphQLErrors?.[0]?.message}
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
