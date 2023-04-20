import React from "react"
import { Autocomplete, Chip, TextField } from "@mui/material"

type MultipleEmailsProps = {
  value: string[]
  onChange: (value: string[]) => void
  margin?: "none" | "dense" | "normal"
  disabled?: boolean
}

const MultipleEmails: React.FC<MultipleEmailsProps> = ({
  value,
  onChange,
  margin,
  disabled,
}) => {
  return (
    <Autocomplete<string, true, false, true>
      multiple
      options={[]}
      disabled={disabled}
      freeSolo
      value={value}
      onChange={(event, newValue) => onChange(newValue)}
      renderTags={(value: readonly string[], getTagProps) =>
        value.map((option: string, index: number) => (
          <Chip variant="outlined" label={option} {...getTagProps({ index })} />
        ))
      }
      renderInput={params => (
        <TextField
          {...params}
          margin={margin}
          placeholder="Enter emails"
          onBlur={event =>
            event.target.value && onChange([...value, event.target.value])
          }
        />
      )}
    />
  )
}

export default MultipleEmails
