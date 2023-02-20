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
import ColumnProperties from "./ColumnProperties"
import ColumnTests from "./ColumnTests"

interface GraiColumnMetadata {
  node_attributes: {
    data_type?: string | null
    is_nullable?: boolean | null
    is_primary_key?: boolean | null
    is_unique?: boolean | null
  }
}

export interface ColumnMetadata {
  grai: GraiColumnMetadata | null
}

interface RequirementEdge {
  metadata?: {
    grai?: {
      edge_attributes: {
        preserves_data_type?: boolean | null
        preserves_nullable?: boolean | null
        preserves_unique?: boolean | null
      }
    }
  } | null
  source: {
    id: string
    name: string
    display_name: string
    metadata: ColumnMetadata
  }
}

export interface Column {
  id: string
  name: string
  display_name: string
  metadata: ColumnMetadata | null
  requirements_edges: RequirementEdge[]
}

type TableColumnsTableProps = {
  search: string | null
  columns: Column[]
}

const TableColumnsTable: React.FC<TableColumnsTableProps> = ({
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
          <TableCell>Data Type</TableCell>
          <TableCell>Properties</TableCell>
          <TableCell>Tests</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {filteredColumns.map((column, index) => (
          <TableRow key={column.id}>
            <TableCell sx={{ color: theme.palette.grey[500], pr: 0 }}>
              {index}
            </TableCell>
            <TableCell sx={{ pl: 1 }}>{column.display_name}</TableCell>
            <TableCell>
              {column.metadata?.grai?.node_attributes.data_type}
            </TableCell>
            <TableCell>
              <ColumnProperties column={column} />
            </TableCell>
            <TableCell>
              <ColumnTests column={column} />
            </TableCell>
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

export default TableColumnsTable
