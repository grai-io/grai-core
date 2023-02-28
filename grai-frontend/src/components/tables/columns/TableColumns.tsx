import React, { ChangeEvent, useState } from "react"
import { CloseFullscreen, OpenInFull, SearchRounded } from "@mui/icons-material"
import { Box, Button, InputAdornment, TextField } from "@mui/material"
import TableColumnsTable, { Column } from "./TableColumnsTable"

type TableColumnsProps = {
  columns: Column[]
}

const TableColumns: React.FC<TableColumnsProps> = ({ columns }) => {
  const [search, setSearch] = useState<string | null>(null)
  const [expanded, setExpanded] = useState<string[]>([])

  const handleSearch = (event: ChangeEvent<HTMLInputElement>) =>
    setSearch(event.target.value)

  const handleExpand = (id: string, expand: boolean) =>
    setExpanded(expand ? [...expanded, id] : expanded.filter(e => e !== id))
  const handleExpandAll = () => setExpanded(columns.map(column => column.id))
  const handleCollapseAll = () => setExpanded([])

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
          {expanded.length > 0 ? (
            <Button
              variant="outlined"
              startIcon={<CloseFullscreen />}
              onClick={handleCollapseAll}
            >
              Collapse all rows
            </Button>
          ) : (
            <Button
              variant="outlined"
              startIcon={<OpenInFull />}
              onClick={handleExpandAll}
            >
              Expand all rows
            </Button>
          )}
        </Box>
      </Box>
      <TableColumnsTable
        search={search}
        columns={columns}
        expanded={expanded}
        onExpand={handleExpand}
      />
    </>
  )
}

export default TableColumns
