import React from "react"
import { MoreHoriz } from "@mui/icons-material"
import { Table, TableBody, TableHead, TableRow } from "@mui/material"
import { useNavigate } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"
import TableCell from "components/tables/TableCell"

interface SourceTable {
  id: string
  display_name: string
  namespace: string
}

type SourceTablesTableProps = {
  tables: SourceTable[]
}

const SourceTablesTable: React.FC<SourceTablesTableProps> = ({ tables }) => {
  const navigate = useNavigate()
  const { routePrefix } = useWorkspace()

  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>Name</TableCell>
          <TableCell>Namespace</TableCell>
          <TableCell sx={{ width: 0 }} />
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
            <TableCell>
              <MoreHoriz />
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}

export default SourceTablesTable
