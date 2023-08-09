import React from "react"
import {
  Chip,
  Stack,
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
import DataSourcesStack from "./DataSourcesStack"

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
          <TableCell>Node Type</TableCell>
          <TableCell>Data Sources</TableCell>
          <TableCell>Active</TableCell>
          <TableCell>Tags</TableCell>
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
            <TableCell>{table.metadata?.grai?.node_type}</TableCell>
            <TableCell sx={{ py: 0, pl: 1 }}>
              <DataSourcesStack data_sources={table.data_sources} />
            </TableCell>
            <TableCell>{table.is_active ? "Yes" : "No"}</TableCell>
            <TableCell sx={{ py: 0 }}>
              <Stack direction="row" spacing={1}>
                {table.metadata?.grai?.tags?.map((tag: string) => (
                  <Chip label={tag} key={tag} />
                ))}
              </Stack>
            </TableCell>
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
