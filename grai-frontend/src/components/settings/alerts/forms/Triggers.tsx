import React from "react"
import {
  Box,
  Typography,
  FormGroup,
  FormControlLabel,
  Checkbox,
} from "@mui/material"

export type Triggers = {
  test_failure?: boolean
}

type TriggersFieldProps = {
  value: Triggers
  onChange: (value: Triggers) => void
  disabled?: boolean
}

const TriggersField: React.FC<TriggersFieldProps> = ({
  value,
  onChange,
  disabled,
}) => (
  <Box sx={{ ml: 1, mt: 1 }}>
    <Typography>Triggers</Typography>
    <FormGroup>
      <FormControlLabel
        disabled={disabled}
        control={
          <Checkbox
            checked={value?.test_failure ?? false}
            onChange={event =>
              onChange({ ...value, test_failure: event.target.checked })
            }
          />
        }
        label="Test Failure"
      />
    </FormGroup>
  </Box>
)

export default TriggersField
