import React, { ChangeEvent, useState } from "react"
import { Button, InputAdornment, TextField } from "@mui/material"

type PasswordFieldProps = {
  label: string
  value: string
  onChange: (event: ChangeEvent<HTMLInputElement>) => void
  required?: boolean
  edit?: boolean
}

const PasswordField: React.FC<PasswordFieldProps> = ({
  label,
  value,
  onChange,
  required,
  edit,
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
      fullWidth
    />
  )
}

export default PasswordField
