import React, { ChangeEvent, useState } from "react"
import { Info } from "@mui/icons-material"
import { Button, InputAdornment, TextField, Tooltip } from "@mui/material"

type PasswordFieldProps = {
  label: string
  value: string
  onChange: (event: ChangeEvent<HTMLInputElement>) => void
  required?: boolean
  edit?: boolean
  helperText?: string | null
}

const PasswordField: React.FC<PasswordFieldProps> = ({
  label,
  value,
  onChange,
  required,
  edit,
  helperText,
}) => {
  const [show, setShow] = useState(!edit)

  const handleShow = () => setShow(true)

  if (!show)
    return (
      <TextField
        label={label}
        value="password"
        margin="normal"
        required={required}
        type="password"
        helperText={helperText}
        fullWidth
        disabled
        InputProps={{
          endAdornment: (
            <InputAdornment position="end">
              <Button onClick={handleShow}>Edit</Button>
            </InputAdornment>
          ),
        }}
      />
    )

  return (
    <TextField
      label={label}
      value={value ?? ""}
      onChange={onChange}
      margin="normal"
      required={required}
      type="password"
      InputProps={{
        endAdornment: helperText ? (
          <InputAdornment position="end" sx={{ cursor: "pointer" }}>
            <Tooltip title={helperText}>
              <Info />
            </Tooltip>
          </InputAdornment>
        ) : null,
      }}
      fullWidth
    />
  )
}

export default PasswordField
