import { OpenInFull, SearchRounded } from "@mui/icons-material"
import { Box, Button, InputAdornment, TextField } from "@mui/material"
import React, { ChangeEvent, useState } from "react"
import NodeColumnsTable from "./NodeColumnsTable"

interface Column {
  id: string
  name: string
  display_name: string
}

type NodeColumnsProps = {
  columns: Column[]
}

const NodeColumns: React.FC<NodeColumnsProps> = ({ columns }) => {
  const [search, setSearch] = useState<string | null>(null)

  const handleSearch = (event: ChangeEvent<HTMLInputElement>) =>
    setSearch(event.target.value)

  return (
    <>
      <Box sx={{ display: "flex", mt: 3 }}>
        <Box sx={{ flexGrow: 1 }}>
          <TextField
            placeholder="Search Columns"
            variant="outlined"
            size="small"
            value={search ?? ""}
            onChange={handleSearch}
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  <SearchRounded />
                </InputAdornment>
              ),
            }}
            sx={{ minWidth: 350 }}
          />
        </Box>
        <Box>
          <Button variant="outlined" startIcon={<OpenInFull />}>
            Expand all rows
          </Button>
        </Box>
      </Box>
      <NodeColumnsTable search={search} columns={columns} />
    </>
  )
}

export default NodeColumns
