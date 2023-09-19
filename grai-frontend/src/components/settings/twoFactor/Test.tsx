import React, { useState } from "react"
import { gql, useMutation } from "@apollo/client"
import { LoadingButton } from "@mui/lab"
import {
  Box,
  Button,
  DialogActions,
  TextField,
  Typography,
} from "@mui/material"
import Form from "components/form/Form"
import GraphError from "components/utils/GraphError"
import {
  ConfirmDevice,
  ConfirmDeviceVariables,
} from "./__generated__/ConfirmDevice"

export const CONFIRM_DEVICE = gql`
  mutation ConfirmDevice($deviceId: ID!, $token: String!) {
    confirmDevice(deviceId: $deviceId, token: $token) {
      id
    }
  }
`

interface Device {
  id: string
}

type TestProps = {
  device: Device
  onBack: () => void
  onClose: () => void
}

const Test: React.FC<TestProps> = ({ device, onBack, onClose }) => {
  const [token, setToken] = useState("")

  const [confirmDevice, { loading, error }] = useMutation<
    ConfirmDevice,
    ConfirmDeviceVariables
  >(CONFIRM_DEVICE)

  const handleSubmit = () => {
    confirmDevice({
      variables: {
        deviceId: device.id,
        token,
      },
    })
      .then(() => onClose())
      .catch(() => {})
  }

  return (
    <Box sx={{ minWidth: 416 }}>
      <Form onSubmit={handleSubmit}>
        <Box sx={{ p: 3 }}>
          <Typography>Enter a code from your authenticator</Typography>
          <TextField
            value={token}
            onChange={event => setToken(event.target.value)}
            margin="normal"
            placeholder="123 456"
            required
            fullWidth
          />
          {error && <GraphError error={error} />}
        </Box>
        <DialogActions sx={{ p: 3, pt: 0 }}>
          <Button variant="outlined" onClick={onBack}>
            Back
          </Button>
          <LoadingButton variant="contained" type="submit" loading={loading}>
            Continue
          </LoadingButton>
        </DialogActions>
      </Form>
    </Box>
  )
}

export default Test
