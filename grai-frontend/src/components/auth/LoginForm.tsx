import React, { useContext, useState } from "react"
import { LoadingButton } from "@mui/lab"
import { Box, TextField } from "@mui/material"
import Form from "components/form/Form"
import AuthContext from "./AuthContext"
import { Link } from "react-router-dom"

type Values = {
  email: string
  password: string
}

const LoginForm: React.FC = () => {
  const { loginUser } = useContext(AuthContext)
  const [values, setValues] = useState<Values>({
    email: "",
    password: "",
  })
  const [loading, setLoading] = useState(false)

  const handleSubmit = async () => {
    setLoading(true)

    await loginUser(values.email, values.password)

    setLoading(false)
  }

  return (
    <Box sx={{ pb: 2 }}>
      <Form onSubmit={handleSubmit}>
        <TextField
          id="email"
          label="Email"
          type="email"
          fullWidth
          margin="normal"
          required
          value={values.email}
          disabled={loading}
          onChange={event =>
            setValues({ ...values, email: event.target.value })
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
