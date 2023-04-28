import React from "react"
import {
  Table,
  TableHead,
  TableRow,
  TableBody,
  Typography,
  TableFooter,
  Tooltip,
  Box,
} from "@mui/material"
import { DateTime } from "luxon"
import { useNavigate } from "react-router-dom"
import { durationAgo } from "helpers/runDuration"
import Loading from "components/layout/Loading"
import TablePagination from "components/table/TablePagination"
import TableCell from "components/tables/TableCell"

interface User {
  id: string
  username: string | null
  first_name: string
  last_name: string
}
interface Filter {
  id: string
  name: string | null
  created_at: string
  created_by: User
}

type FiltersTableProps = {
  filters: Filter[]
  workspaceId: string
  loading?: boolean
  total: number
}

const FiltersTable: React.FC<FiltersTableProps> = ({
  filters,
  workspaceId,
  loading,
  total,
}) => {
  const navigate = useNavigate()

  return (
    <Table>
      <TableHead>
        <TableRow sx={{ backgroundColor: theme => theme.palette.grey[100] }}>
          <TableCell>Name</TableCell>
          <TableCell sx={{ textAlign: "right" }}>Created</TableCell>
          <TableCell>User</TableCell>
          <TableCell sx={{ width: 0 }} />
        </TableRow>
      </TableHead>
      <TableBody>
        {filters.map(filter => (
          <TableRow
            key={filter.id}
            hover
            sx={{ cursor: "pointer" }}
            onClick={() => navigate(filter.id)}
          >
            <TableCell>{filter.name}</TableCell>
            <TableCell sx={{ textAlign: "right" }}>
              <Box>
                <Tooltip
                  title={DateTime.fromISO(filter.created_at).toLocaleString(
                    DateTime.DATETIME_FULL_WITH_SECONDS
                  )}
                >
                  <Typography variant="body2">
                    {durationAgo(filter.created_at, 1)} ago
                  </Typography>
                </Tooltip>
              </Box>
            </TableCell>
            <TableCell>{filter.created_by.first_name}</TableCell>
            <TableCell sx={{ py: 0, px: 1 }} stopPropagation>
              {/* <ConnectionsMenu
                connection={connection}
                workspaceId={workspaceId}
              /> */}
            </TableCell>
          </TableRow>
        ))}
        {!loading && filters.length === 0 && (
          <TableRow>
            <TableCell colSpan={99} sx={{ textAlign: "center", py: 10 }}>
              <Typography>No filters found</Typography>
            </TableCell>
          </TableRow>
        )}
        {loading && (
          <TableRow>
            <TableCell colSpan={99}>
              <Loading />
            </TableCell>
          </TableRow>
        )}
      </TableBody>
      <TableFooter>
        <TablePagination
          count={total}
          rowsPerPage={1000}
          page={0}
          type="connections"
        />
      </TableFooter>
    </Table>
  )
}

export default FiltersTable
