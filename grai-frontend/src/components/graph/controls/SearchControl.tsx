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
          endAdornment: (
            <InputAdornment position="end">
              {value ? (
                <Close onClick={handleClear} sx={{ cursor: "pointer" }} />
              ) : (
                <Search />
              )}
            </InputAdornment>
          ),
        }}
        sx={{ backgroundColor: "white", width: 240 }}
      />
    </Box>
  )
}

export default SearchControl
