import React, { useEffect, useState } from "react"
import { gql, useMutation } from "@apollo/client"
import { LoadingButton } from "@mui/lab"
import {
  Box,
  Button,
  List,
  ListItemButton,
  TextField,
  Typography,
} from "@mui/material"
import posthog from "posthog"
import Form from "components/form/Form"
import GraphError from "components/utils/GraphError"
import {
  LoginWithToken,
  LoginWithTokenVariables,
} from "./__generated__/LoginWithToken"
import { Device } from "./LoginWrapper"
import useAuth from "../useAuth"

export const LOGIN = gql`
  mutation LoginWithToken(
    $username: String!
    $password: String!
    $deviceId: ID!
    $token: String!
  ) {
    loginWithToken(
      username: $username
      password: $password
      deviceId: $deviceId
      token: $token
    ) {
      id
      username
      first_name
      last_name
    }
  }
`

type TokenFormProps = {
  username: string
  password: string
  devices: Device[]
  onBack: () => void
}

const TokenForm: React.FC<TokenFormProps> = ({
  username,
  password,
  devices,
  onBack,
}) => {
  const { setLoggedIn } = useAuth()
  const [device, setDevice] = useState<Device>()
  const [token, setToken] = useState("")

  const [login, { loading, error }] = useMutation<
    LoginWithToken,
    LoginWithTokenVariables
  >(LOGIN)

  useEffect(() => {
    if (devices.length === 1) {
      setDevice(devices[0])
    }
  }, [devices, setDevice])

  if (device) {
    const handleSubmit = () =>
      login({
        variables: {
          username,
          password,
          deviceId: device.id,
          token,
        },
      })
        .then(data => data.data?.loginWithToken)
        .then(res => {
          if (!res) return

          posthog.identify(res.id, { email: res.username })
          setLoggedIn(true)
        })
        .catch(() => {})

    return (
      <>
        <Typography>Two Factor Authentication</Typography>
        <Typography>Please enter the 6 digit code from your device</Typography>
        <Typography>{device.name}</Typography>
        <Form onSubmit={handleSubmit}>
          <TextField
            value={token}
            onChange={event => setToken(event.target.value)}
            placeholder="123 456"
            margin="normal"
            required
            fullWidth
          />
          {error && <GraphError error={error} />}
          <Box sx={{ display: "flex", mt: 2 }}>
            <Button variant="outlined" onClick={() => setDevice(undefined)}>
              Back
            </Button>
            <Box sx={{ flexGrow: 1 }} />
            <LoadingButton variant="contained" type="submit" loading={loading}>
              Continue
            </LoadingButton>
          </Box>
        </Form>
      </>
    )
  }

  return (
    <>
      <Typography>Two Factor Authentication</Typography>
      <Typography>Select a device</Typography>
      <List>
        {devices.map(device => (
          <ListItemButton key={device.id} onClick={() => setDevice(device)}>
            {device.name}
          </ListItemButton>
        ))}
      </List>
      <Button variant="outlined" onClick={onBack}>
        Back
      </Button>
    </>
  )
}

export default TokenForm
