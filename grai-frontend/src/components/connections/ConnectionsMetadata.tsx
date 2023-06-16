import React from "react"
import { ConnectorType, ConnectorMetadataField } from "./ConnectionsForm"
import BooleanField from "./fields/BooleanField"
import PasswordField from "./fields/PasswordField"
import TextField from "./fields/TextField"

type ConnectionsMetadataProps = {
  connector: ConnectorType
  metadata: any
  secrets: any
  onChangeMetadata: (value: any) => void
  onChangeSecrets: (value: any) => void
  edit?: boolean
}

const ConnectionsMetadata: React.FC<ConnectionsMetadataProps> = ({
  connector,
  metadata,
  secrets,
  onChangeMetadata,
  onChangeSecrets,
  edit,
}) => {
  const handleChangeMetadata = (
    mValue: string | boolean,
    field: ConnectorMetadataField
  ) => {
    const newValue = { ...metadata }
    newValue[field.name] = mValue
    onChangeMetadata(newValue)
  }

  const handleChangeSecrets = (
    mValue: string,
    field: ConnectorMetadataField
  ) => {
    const newValue = { ...secrets }
    newValue[field.name] = mValue
    onChangeSecrets(newValue)
  }

  const fields = [...(connector.metadata?.fields ?? [])]

  const orderSort = (a: { order?: number }, b: { order?: number }) =>
    (a.order ?? 0) > (b.order ?? 0) ? 1 : -1

  return (
    <>
      {fields
        ?.sort(orderSort)
        .map(field =>
          field.secret ? (
            <PasswordField
              key={field.name}
              label={field.label ?? field.name}
              value={secrets && secrets[field.name]}
              onChange={event => handleChangeSecrets(event.target.value, field)}
              required={field.required}
              helperText={field.helper_text}
              edit={edit}
            />
          ) : field.type && field.type === "boolean" ? (
            <BooleanField
              key={field.name}
              value={
                (metadata && metadata[field.name]) ?? field.default ?? false
              }
              onChange={value => handleChangeMetadata(value, field)}
              label={field.label ?? field.name}
              helperText={field.helper_text}
            />
          ) : (
            <TextField
              key={field.name}
              label={field.label ?? field.name}
              type={field.type}
              value={(metadata && metadata[field.name]) ?? ""}
              onChange={value => handleChangeMetadata(value, field)}
              required={field.required}
              helperText={field.helper_text}
            />
          )
        )}
    </>
  )
}

export default ConnectionsMetadata
