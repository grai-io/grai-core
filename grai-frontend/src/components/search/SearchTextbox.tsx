import React from "react"
import { Close, Search } from "@mui/icons-material"
import { Box, Button, InputAdornment, TextField } from "@mui/material"
import { useSearchBox } from "react-instantsearch-hooks-web"

type SearchTextboxProps = {
  onClose: () => void
}

const SearchTextbox: React.FC<SearchTextboxProps> = ({ onClose }) => {
  const { query, refine, clear } = useSearchBox()

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) =>
    refine(event.target.value)

  return (
    <Box sx={{ display: "flex" }}>
      <TextField
        variant="standard"
        value={query}
        onChange={handleChange}
        placeholder="Search"
        fullWidth
        autoFocus
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <Search fontSize="large" />
            </InputAdornment>
          ),
          endAdornment:
            query.length > 0 ? (
              <InputAdornment position="end" onClick={clear}>
                <Close sx={{ cursor: "pointer" }} />
              </InputAdornment>
            ) : null,
          disableUnderline: true,
          sx: { p: 2, fontSize: 20 },
        }}
      />
      <Box sx={{ borderRight: 1, borderColor: "divider", my: 1 }} />
      <Button onClick={onClose} sx={{ m: 1 }}>
        Close
      </Button>
    </Box>
  )
}

export default SearchTextbox
