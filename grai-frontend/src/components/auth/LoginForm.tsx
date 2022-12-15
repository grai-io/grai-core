import React, { useContext, useState } from "react"
import { LoadingButton } from "@mui/lab"
import { TextField } from "@mui/material"
import Form from "components/form/Form"
import AuthContext from "./AuthContext"

const LoginForm: React.FC = () => {
  const { loginUser } = useContext(AuthContext)
  const [email, setEmail] = useState<string>("")
  const [password, setPassword] = useState<string>("")
  const [loading, setLoading] = useState(false)

  const handleSubmit = async () => {
    setLoading(true)

    await loginUser(email, password)

    setLoading(false)
  }

  const handlePasswordChange: React.ChangeEventHandler<
    HTMLInputElement
  > = event => {
    setPassword(event.target.value)
  }

  return (
    <Form onSubmit={handleSubmit}>
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
      <TextField
        inputProps={{ "data-testid": "password" }}
        label="Password"
        type="password"
        fullWidth
        margin="normal"
        required
        value={password}
        disabled={loading}
        onChange={handlePasswordChange}
      />
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
  )
}

export default LoginForm
