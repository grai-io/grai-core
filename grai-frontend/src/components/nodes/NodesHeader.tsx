import { Refresh, Search } from "@mui/icons-material"
import {
  Box,
  Button,
  InputAdornment,
  TextField,
  Tooltip,
  Typography,
} from "@mui/material"
import React, { ChangeEvent } from "react"

type NodesHeaderProps = {
  search?: string | null
  onSearch?: (value: string) => void
  onRefresh?: () => void
}

const NodesHeader: React.FC<NodesHeaderProps> = ({
  search,
  onSearch,
  onRefresh,
}) => {
  const handleSearch = (event: ChangeEvent<HTMLInputElement>) =>
    onSearch && onSearch(event.target.value)

  return (
    <Box sx={{ display: "flex", m: 3 }}>
      <Typography variant="h4" sx={{ flexGrow: "1" }}>
        Tables
      </Typography>
      <Box>
        <TextField
          placeholder="Search"
          value={search ?? ""}
          onChange={handleSearch}
          size="small"
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <Search />
              </InputAdornment>
            ),
          }}
          sx={{ mr: 2, minWidth: 300 }}
        />
        <Tooltip title="Refresh table">
          <Button
            variant="outlined"
            sx={{ width: 40, height: 40, minWidth: 0 }}
            onClick={onRefresh}
            size="small"
          >
            <Refresh />
          </Button>
        </Tooltip>
      </Box>
    </Box>
  )
}

export default NodesHeader
