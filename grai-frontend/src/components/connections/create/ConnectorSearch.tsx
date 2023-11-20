import React from "react"
import { Search } from "@mui/icons-material"
import { InputAdornment, TextField } from "@mui/material"

type ConnectorSearchProps = {
  value: string
  onChange: (value: string) => void
}

const ConnectorSearch: React.FC<ConnectorSearchProps> = ({
  value,
  onChange,
}) => (
  <TextField
    value={value}
    onChange={event => onChange(event.target.value)}
    placeholder="Search"
    size="small"
    InputProps={{
      endAdornment: (
        <InputAdornment position="end">
          <Search fontSize="small" />
        </InputAdornment>
      ),
    }}
  />
)

export default ConnectorSearch
