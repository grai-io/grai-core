import React from "react"
import { Info } from "@mui/icons-material"
import {
  Box,
  Checkbox,
  FormControlLabel,
  FormGroup,
  Tooltip,
} from "@mui/material"

type BooleanFieldProps = {
  value: boolean
  onChange: (value: boolean) => void
  label: string
  helperText?: string | null
}

const BooleanField: React.FC<BooleanFieldProps> = ({
  value,
  onChange,
  label,
  helperText,
}) => (
  <Box sx={{ display: "flex", alignItems: "center" }}>
    <FormGroup>
      <FormControlLabel
        control={<Checkbox checked={value} />}
        label={label}
        onChange={(event, checked) => onChange(checked)}
      />
    </FormGroup>
    {helperText && (
      <Tooltip title={helperText}>
        <Info sx={{ color: "rgba(0, 0, 0, 0.54)", cursor: "pointer" }} />
      </Tooltip>
    )}
  </Box>
)

export default BooleanField
