import React from "react"
import { ListItemText, MenuItem, TextField } from "@mui/material"

type MembershipRoleProps = {
  value: string
  onChange: (value: string) => void
  required?: boolean
  disabled?: boolean
}

const MembershipRole: React.FC<MembershipRoleProps> = ({
  value,
  onChange,
  required,
  disabled,
}) => (
  <TextField
    select
    value={value}
    onChange={event => onChange(event.target.value)}
    fullWidth
    required={required}
    margin="normal"
    disabled={disabled}
    inputProps={{ "data-testid": "role-select" }}
  >
    <MenuItem value="admin">
      <ListItemText primary="Admin" secondary="Can add and remove members" />
    </MenuItem>
    <MenuItem value="member">
      <ListItemText
        primary="Member"
        secondary="Can edit but not add or remove members"
      />
    </MenuItem>
    <MenuItem value="read_only">
      <ListItemText primary="Read Only" secondary="Can only view data" />
    </MenuItem>
  </TextField>
)

export default MembershipRole
