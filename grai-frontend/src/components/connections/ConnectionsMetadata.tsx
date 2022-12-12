import { TextField } from "@mui/material"
import React from "react"
import { ConnectorType } from "../form/fields/Connector"

type ConnectionsMetadataProps = {
  connector: ConnectorType
  value: any
  onChange: (value: any) => void
}

const ConnectionsMetadata: React.FC<ConnectionsMetadataProps> = ({
  connector,
  value,
  onChange,
}) => {
  const handleChange = (mValue: string, name: string) => {
    let newValue = { ...value }
    newValue[name] = mValue
    onChange(newValue)
  }

  return (
    <>
      {connector.metadata?.fields?.map(field => (
        <TextField
          key={field.name}
          label={field.label ?? field.name}
          value={(value && value[field.name]) ?? ""}
          onChange={event => handleChange(event.target.value, field.name)}
          margin="normal"
          required={field.required}
          type={field.secret ? "password" : "text"}
          fullWidth
        />
      ))}
    </>
  )
}

export default ConnectionsMetadata
