import React from "react"
import {
  Table,
  TableBody,
  TableFooter,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material"
import { useNavigate } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"
import Loading from "components/layout/Loading"
import TablePagination from "components/table/TablePagination"
import TableCell from "components/tables/TableCell"

interface SourceTable {
  id: string
  display_name: string
  namespace: string
}

type SourceTablesTableProps = {
  tables: SourceTable[]
  loading?: boolean
  total: number
  page: number
  onPageChange: (page: number) => void
}

const SourceTablesTable: React.FC<SourceTablesTableProps> = ({
  tables,
  loading,
  total,
  page,
  onPageChange,
}) => {
  const navigate = useNavigate()
  const { routePrefix } = useWorkspace()

  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>Name</TableCell>
          <TableCell>Namespace</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {tables.map(table => (
          <TableRow
            key={table.id}
            hover
            onClick={() => navigate(`${routePrefix}/tables/${table.id}`)}
            sx={{ cursor: "pointer" }}
          >
            <TableCell>{table.display_name}</TableCell>
            <TableCell>{table.namespace}</TableCell>
          </TableRow>
        ))}
        {loading && (
          <TableRow>
            <TableCell colSpan={99}>
              <Loading />
            </TableCell>
          </TableRow>
        )}
        {!loading && tables.length === 0 && (
          <TableRow>
            <TableCell colSpan={99} sx={{ py: 10, textAlign: "center" }}>
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
          onPageChange={onPageChange}
          type="tables"
        />
      </TableFooter>
    </Table>
  )
}

export default SourceTablesTable
