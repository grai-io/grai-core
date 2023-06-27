import React, { ChangeEvent } from "react"
import { Refresh, Search } from "@mui/icons-material"
import { Box, TextField, InputAdornment, Tooltip, Button } from "@mui/material"

type TableHeaderProps = {
  search?: string | null
  onSearch?: (value: string) => void
  onRefresh?: () => void
  rightButtons?: React.ReactNode
  children?: React.ReactNode
}

const TableHeader: React.FC<TableHeaderProps> = ({
  search,
  onSearch,
  onRefresh,
  rightButtons,
  children,
}) => {
  const handleSearch = (event: ChangeEvent<HTMLInputElement>) =>
    onSearch && onSearch(event.target.value)

  return (
    <Box sx={{ display: "flex", mb: "24px" }}>
      <Box sx={{ flexGrow: 1, display: "flex" }}>
        {onSearch && (
          <TextField
            placeholder="Search"
            value={search ?? ""}
            onChange={handleSearch}
            size="small"
            data-testid="table-search"
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  <Search />
                </InputAdornment>
              ),
            }}
            sx={{ mr: 2, minWidth: 300 }}
          />
        )}
        {children}
      </Box>
      {onRefresh && (
        <Tooltip title="Refresh table">
          <Button
            variant="outlined"
            sx={{ width: 40, height: 40, minWidth: 0 }}
            onClick={onRefresh}
            size="small"
            data-testid="table-refresh"
          >
            <Refresh />
          </Button>
        </Tooltip>
      )}
      {rightButtons}
    </Box>
  )
}

export default TableHeader
