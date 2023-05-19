import React from "react"
import {
  Table,
  TableBody,
  TableCell,
  TableFooter,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material"
import { useNavigate } from "react-router-dom"
import { Table as TableInterface } from "pages/tables/Tables"
import Loading from "components/layout/Loading"
import TablePagination from "components/table/TablePagination"

type TablesTableProps = {
  tables: TableInterface[]
  loading?: boolean
  total: number
  page: number
  onPageChange: (page: number) => void
}

const TablesTable: React.FC<TablesTableProps> = ({
  tables,
  loading,
  total,
  page,
  onPageChange,
}) => {
  const navigate = useNavigate()

  return (
    <Table sx={{ mb: -1 }}>
      <TableHead>
        <TableRow>
          <TableCell>Name</TableCell>
          <TableCell>Namespace</TableCell>
          <TableCell>Data Source</TableCell>
          <TableCell>Active</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {tables.map(table => (
          <TableRow
            key={table.id}
            onClick={() => navigate(table.id)}
            hover
            sx={{
              cursor: "pointer",
            }}
          >
            <TableCell>{table.display_name ?? table.name}</TableCell>
            <TableCell>{table.namespace}</TableCell>
            <TableCell>{table.data_source}</TableCell>
            <TableCell>{table.is_active ? "Yes" : "No"}</TableCell>
          </TableRow>
        ))}
        {loading && (
          <TableRow>
            <TableCell colSpan={99}>
              <Loading />
            </TableCell>
          </TableRow>
        )}
        {tables.length === 0 && !loading && (
          <TableRow>
            <TableCell colSpan={99} sx={{ textAlign: "center", py: 10 }}>
              <Typography>No tables found</Typography>
            </TableCell>
          </TableRow>
        )}
      </TableBody>
      <TableFooter>
        <TablePagination
          count={total}
          rowsPerPage={20}
          page={page}
          type="tables"
          onPageChange={onPageChange}
        />
      </TableFooter>
    </Table>
  )
}

export default TablesTable
