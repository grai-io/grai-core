import React from "react"
import { MenuItem, TextField } from "@mui/material"
import { DatePicker } from "@mui/x-date-pickers/DatePicker"
import { DateTime } from "luxon"

export type ExpiryDate = number | "none" | "custom" | DateTime | null

type ExpirationFieldProps = {
  value: ExpiryDate
  onChange: (value: ExpiryDate) => void
  required?: boolean
  disabled?: boolean
}

const ExpirationField: React.FC<ExpirationFieldProps> = ({
  value,
  onChange,
  required,
  disabled,
}) => {
  const isCustom = typeof value === "object" || value === "custom"

  const selectValue = isCustom ? "custom" : value

  return (
    <>
      <TextField
        select
        value={selectValue}
        onChange={event =>
          onChange(event.target.value as number | "none" | null)
        }
        fullWidth
        required={required}
        margin="normal"
        disabled={disabled}
        label="Expiration"
        inputProps={{ "data-testid": "expiration-select" }}
      >
        <MenuItem value={7}>7 days</MenuItem>
        <MenuItem value={30}>30 days</MenuItem>
        <MenuItem value={60}>60 days</MenuItem>
        <MenuItem value={90}>90 days</MenuItem>
        <MenuItem value="custom">Custom</MenuItem>
        <MenuItem value="none">No expiration</MenuItem>
      </TextField>

      {isCustom && (
        <DatePicker
          value={value}
          onChange={value => onChange(value)}
          slots={{
            textField: props => (
              <TextField
                {...props}
                fullWidth
                margin="normal"
                disabled={disabled}
                required
                inputProps={{
                  "data-testid": "date-input",
                  ...props.inputProps,
                }}
              />
            ),
          }}
        />
      )}
    </>
  )
}

export default ExpirationField
