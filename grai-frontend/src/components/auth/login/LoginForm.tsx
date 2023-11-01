import React, { useState } from "react"
import { gql, useMutation } from "@apollo/client"
import { LoadingButton } from "@mui/lab"
import { Box, InputLabel, Link, TextField, styled } from "@mui/material"
import hubspot from "hubspot"
import posthog from "posthog"
import { Link as RouterLink } from "react-router-dom"
import Form from "components/form/Form"
import GraphError from "components/utils/GraphError"
import { Login, LoginVariables } from "./__generated__/Login"
import { DeviceRequest } from "./LoginWrapper"
import useAuth from "../useAuth"

export const LOGIN = gql`
  mutation Login($username: String!, $password: String!) {
    login(username: $username, password: $password) {
      ... on User {
        id
        username
        first_name
        last_name
      }
      ... on DeviceDataWrapper {
        data {
          id
          name
        }
      }
    }
  }
`

const StyledInputLabel = styled(InputLabel)(theme => ({
  fontWeight: 600,
  fontSize: 14,
  color: "#263238",
  marginBottom: theme.theme.spacing(1),
}))

type Values = {
  username: string
  password: string
}

type LoginFormProps = {
  onDeviceRequest: (request: DeviceRequest) => void
}

const LoginForm: React.FC<LoginFormProps> = ({ onDeviceRequest }) => {
  const { setLoggedIn } = useAuth()
  const [values, setValues] = useState<Values>({
    username: "",
    password: "",
  })

  const [login, { loading, error }] = useMutation<Login, LoginVariables>(LOGIN)

  const handleSubmit = () =>
    login({ variables: values })
      .then(data => data.data?.login)
      .then(res => {
        if (!res) return

        if (res.__typename === "User") {
          posthog.identify(res.id, { email: res.username })
          hubspot.push(["identify", { email: res.username }])
          setLoggedIn(true)
          return
        }

        onDeviceRequest({
          devices: res.data,
          username: values.username,
          password: values.password,
        })
      })
      .catch(() => {})

  return (
    <Box>
      <Form onSubmit={handleSubmit}>
        {error && <GraphError error={error} />}
        <StyledInputLabel>Email</StyledInputLabel>
        <TextField
          inputProps={{ "data-testid": "email" }}
          placeholder="yourname@mail.com"
          type="email"
          fullWidth
          required
          value={values.username}
          disabled={loading}
          onChange={event =>
            setValues({ ...values, username: event.target.value })
          }
          InputProps={{
            sx: { borderRadius: "8px" },
          }}
        />
        <StyledInputLabel
          sx={{
            mt: 2,
          }}
        >
          Password
        </StyledInputLabel>
        <TextField
          inputProps={{ "data-testid": "password" }}
          placeholder="********"
          type="password"
          fullWidth
          required
          value={values.password}
          disabled={loading}
          error={!!error}
          onChange={event =>
            setValues({ ...values, password: event.target.value })
          }
          InputProps={{
            sx: { borderRadius: "8px" },
          }}
        />
        <Box sx={{ mt: 2, mb: 2 }}>
          <Link
            component={RouterLink}
            to="/forgot"
            sx={{
              textDecoration: "none",
              fontSize: 14,
              fontWeight: 600,
              fontFamily: `"Sora", "Satoshi", "Roboto", "Helvetica", "Arial", sans-serif`,
              "&:hover": {
                color: theme => theme.palette.grey[600],
              },
            }}
          >
            Forgot your password?
          </Link>
        </Box>
        <LoadingButton
          variant="contained"
          fullWidth
          type="submit"
          size="large"
          loading={loading}
          sx={{
            height: 56,
            mt: 2,
            color: "white",
            backgroundColor: "#FC6016",
            fontSize: 18,
            fontWeight: 600,
            borderRadius: "8px",
            boxShadow: "0px 4px 6px #FC601620",
          }}
        >
          Log In
        </LoadingButton>
      </Form>
    </Box>
  )
}

export default LoginForm
