import React from "react"
import { Info } from "@mui/icons-material"
import {
  TextField as BaseTextField,
  InputAdornment,
  Tooltip,
} from "@mui/material"

type TextFieldProps = {
  label: string
  type?: string | null
  value: string
  onChange: (value: string) => void
  required?: boolean
  helperText?: string | null
}

const TextField: React.FC<TextFieldProps> = ({
  label,
  type,
  value,
  onChange,
  required,
  helperText,
}) => (
  <BaseTextField
    label={label}
    type={type ?? "text"}
    value={value}
    onChange={event => onChange(event.target.value)}
    margin="normal"
    required={required}
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

export default TextField
