import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material"
import React from "react"
import theme from "theme"

interface Column {
  id: string
  name: string
  display_name: string
}

type NodeColumnsTableProps = {
  search: string | null
  columns: Column[]
}

const NodeColumnsTable: React.FC<NodeColumnsTableProps> = ({
  search,
  columns,
}) => {
  const filteredColumns = search
    ? columns.filter(column =>
        column.name.toLowerCase().includes(search.toLowerCase())
      )
    : columns

  return (
    <Table sx={{ mt: 1 }}>
      <TableHead sx={{ backgroundColor: theme.palette.grey[100] }}>
        <TableRow>
          <TableCell sx={{ width: 0 }} />
          <TableCell>Name</TableCell>
          <TableCell>Lineage</TableCell>
          <TableCell>Completeness</TableCell>
          <TableCell>Distribution</TableCell>
          <TableCell>Description</TableCell>
          <TableCell>Tags</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {filteredColumns.map((column, index) => (
          <TableRow key={column.id}>
            <TableCell sx={{ color: theme.palette.grey[500], pr: 0 }}>
              {index}
            </TableCell>
            <TableCell sx={{ pl: 1 }}>{column.display_name}</TableCell>
            <TableCell />
            <TableCell />
            <TableCell />
            <TableCell />
            <TableCell />
          </TableRow>
        ))}
        {filteredColumns.length === 0 && (
          <TableRow>
            <TableCell colSpan={99} sx={{ textAlign: "center", py: 10 }}>
              <Typography>No columns found</Typography>
              {search && (
                <Typography sx={{ mt: 2 }}>Try clearing search</Typography>
              )}
            </TableCell>
          </TableRow>
        )}
      </TableBody>
    </Table>
  )
}

export default NodeColumnsTable
