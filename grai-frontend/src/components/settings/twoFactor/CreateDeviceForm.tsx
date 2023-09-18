import React, { useEffect, useState } from "react"
import { gql, useMutation } from "@apollo/client"
import Loading from "components/layout/Loading"
import GraphError from "components/utils/GraphError"
import {
  CreateDevice,
  CreateDeviceVariables,
} from "./__generated__/CreateDevice"
import Code from "./Code"
import Test from "./Test"

export const CREATE_DEVICE = gql`
  mutation CreateDevice($name: String!) {
    createDevice(name: $name) {
      id
      name
      config_url
    }
  }
`

export interface Device {
  id: string
  config_url: string
}

type CreateDeviceFormProps = {
  onClose: () => void
}

const CreateDeviceForm: React.FC<CreateDeviceFormProps> = ({ onClose }) => {
  const [next, setNext] = useState(false)

  const [createDevice, { loading, error, data }] = useMutation<
    CreateDevice,
    CreateDeviceVariables
  >(CREATE_DEVICE)

  useEffect(() => {
    createDevice({
      variables: {
        name: "TOTP",
      },
    }).catch(() => {})
  }, [createDevice])

  if (error) return <GraphError error={error} />
  if (loading) return <Loading />

  if (!data?.createDevice) return null

  if (next)
    return (
      <Test
        device={data.createDevice}
        onClose={onClose}
        onBack={() => setNext(false)}
      />
    )

  return (
    <Code
      config_url={data.createDevice.config_url}
      onNext={() => setNext(true)}
    />
  )
}

export default CreateDeviceForm
