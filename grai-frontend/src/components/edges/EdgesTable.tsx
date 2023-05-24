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
import Loading from "components/layout/Loading"
import TablePagination from "components/table/TablePagination"

interface Edge {
  id: string
  name: string
  display_name: string
  namespace: string
  data_source: string
  is_active: boolean
}

type EdgesTableProps = {
  edges: Edge[]
  loading?: boolean
  total: number
}

const EdgesTable: React.FC<EdgesTableProps> = ({ edges, loading, total }) => {
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
        {edges.map(edge => (
          <TableRow
            key={edge.id}
            onClick={() => navigate(edge.id)}
            hover
            sx={{
              cursor: "pointer",
            }}
          >
            <TableCell>{edge.display_name ?? edge.name}</TableCell>
            <TableCell>{edge.namespace}</TableCell>
            <TableCell>{edge.data_source}</TableCell>
            <TableCell>{edge.is_active ? "Yes" : "No"}</TableCell>
          </TableRow>
        ))}
        {loading && (
          <TableRow>
            <TableCell colSpan={99}>
              <Loading />
            </TableCell>
          </TableRow>
        )}
        {edges.length === 0 && !loading && (
          <TableRow>
            <TableCell colSpan={99} sx={{ textAlign: "center", py: 10 }}>
              <Typography>No edges found</Typography>
            </TableCell>
          </TableRow>
        )}
      </TableBody>
      <TableFooter>
        <TablePagination
          count={total}
          rowsPerPage={1000}
          page={0}
          type="edges"
        />
      </TableFooter>
    </Table>
  )
}

export default EdgesTable
