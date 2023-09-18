import React, { useState } from "react"
import LoginForm from "./LoginForm"
import TokenForm from "./TokenForm"

export interface DeviceRequest {
  username: string
  password: string
  devices: Device[]
}

export interface Device {
  id: string
  name: string
}

const LoginWrapper: React.FC = () => {
  const [request, setRequest] = useState<DeviceRequest>()

  if (request)
    return (
      <TokenForm
        username={request.username}
        password={request.password}
        devices={request.devices}
        onBack={() => setRequest(undefined)}
      />
    )

  return <LoginForm onDeviceRequest={setRequest} />
}

export default LoginWrapper
