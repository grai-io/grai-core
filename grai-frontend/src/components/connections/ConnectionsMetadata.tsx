import React from "react"
import { Info } from "@mui/icons-material"
import {
  Box,
  Checkbox,
  FormControlLabel,
  FormGroup,
  InputAdornment,
  TextField,
  Tooltip,
} from "@mui/material"
import { ConnectorType, ConnectorMetadataField } from "./ConnectionsForm"
import PasswordField from "./fields/PasswordField"

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
    let newValue = { ...metadata }
    newValue[field.name] = mValue
    onChangeMetadata(newValue)
  }

  const handleChangeSecrets = (
    mValue: string,
    field: ConnectorMetadataField
  ) => {
    let newValue = { ...secrets }
    newValue[field.name] = mValue
    onChangeSecrets(newValue)
  }

  const fields = [...(connector.metadata?.fields ?? [])]

  return (
    <>
      {fields
        ?.sort((a, b) => ((a.order ?? 0) > (b.order ?? 0) ? 1 : -1))
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
            <Box
              sx={{ display: "flex", alignItems: "center" }}
              key={field.name}
            >
              <FormGroup>
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={
                        (metadata && metadata[field.name]) ??
                        field.default ??
                        false
                      }
                    />
                  }
                  label={field.label ?? field.name}
                  onChange={(event, checked) =>
                    handleChangeMetadata(checked, field)
                  }
                />
              </FormGroup>
              {field.helper_text && (
                <Tooltip title={field.helper_text}>
                  <Info
                    sx={{ color: "rgba(0, 0, 0, 0.54)", cursor: "pointer" }}
                  />
                </Tooltip>
              )}
            </Box>
          ) : (
            <TextField
              key={field.name}
              label={field.label ?? field.name}
              type={field.type ?? "text"}
              value={(metadata && metadata[field.name]) ?? ""}
              onChange={event =>
                handleChangeMetadata(event.target.value, field)
              }
              margin="normal"
              required={field.required}
              InputProps={{
                endAdornment: field.helper_text ? (
                  <InputAdornment position="end" sx={{ cursor: "pointer" }}>
                    <Tooltip title={field.helper_text}>
                      <Info />
                    </Tooltip>
                  </InputAdornment>
                ) : null,
              }}
              fullWidth
            />
          )
        )}
    </>
  )
}

export default ConnectionsMetadata
