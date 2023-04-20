import React from "react"
import { MenuItem, TextField } from "@mui/material"

type ChannelProps = {
  value: string
  onChange: (value: string) => void
}

const options = [
  {
    value: "email",
    label: "Email",
    // icon: <Email />,
  },
  {
    value: "slack",
    label: "Slack",
    disabled: true,
  },
  {
    value: "pager-duty",
    label: "PageDuty",
    disabled: true,
  },
]

const Channel: React.FC<ChannelProps> = ({ value, onChange }) => (
  <TextField
    label="Channel"
    value={value}
    onChange={event => onChange(event.target.value)}
    select
    fullWidth
    margin="normal"
    inputProps={{ "data-testid": "channel-select" }}
  >
    {options.map(option => (
      <MenuItem
        value={option.value}
        key={option.value}
        disabled={option.disabled}
      >
        {option.label}
        {/* <ListItemIcon>{option.icon}</ListItemIcon>
        <ListItemText>{option.label}</ListItemText> */}
      </MenuItem>
    ))}
  </TextField>
)

export default Channel
