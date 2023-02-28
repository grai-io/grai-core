import React from "react"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material"
import { useNavigate } from "react-router-dom"
import { Table as TableInterface } from "pages/tables/Tables"
import Loading from "components/layout/Loading"

type TablesTableProps = {
  tables: TableInterface[]
  loading?: boolean
}

const TablesTable: React.FC<TablesTableProps> = ({ tables, loading }) => {
  const navigate = useNavigate()

  return (
    <Table>
      <TableHead>
        <TableRow sx={{ backgroundColor: theme => theme.palette.grey[100] }}>
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
    </Table>
  )
}

export default TablesTable
