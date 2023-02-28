import React, { ChangeEvent } from "react"
import { Close, Search } from "@mui/icons-material"
import { Box, TextField, InputAdornment } from "@mui/material"

type SearchControlProps = {
  value: string | null
  onChange: (value: string | null) => void
}

const SearchControl: React.FC<SearchControlProps> = ({ value, onChange }) => {
  const handleChange = (event: ChangeEvent<HTMLInputElement>) =>
    onChange(event.target.value)

  const handleClear = () => onChange(null)

  return (
    <Box>
      <TextField
        value={value ?? ""}
        onChange={handleChange}
        placeholder="Search"
        size="small"
        inputProps={{
          "data-testid": "search-input",
        }}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <Search />
            </InputAdornment>
          ),
          endAdornment: value ? (
            <InputAdornment position="end">
              <Close onClick={handleClear} sx={{ cursor: "pointer" }} />
            </InputAdornment>
          ) : undefined,
        }}
        sx={{ backgroundColor: "white", width: 350 }}
      />
    </Box>
  )
}

export default SearchControl
