import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material"
import React from "react"
import { useNavigate } from "react-router-dom"
import { Node } from "pages/nodes/Nodes"
import Loading from "components/layout/Loading"

type NodesTableProps = {
  nodes: Node[]
  loading?: boolean
}

const NodesTable: React.FC<NodesTableProps> = ({ nodes, loading }) => {
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
        {nodes.map(node => (
          <TableRow
            key={node.id}
            onClick={() => navigate(node.id)}
            hover
            sx={{
              cursor: "pointer",
            }}
          >
            <TableCell>{node.display_name ?? node.name}</TableCell>
            <TableCell>{node.namespace}</TableCell>
            <TableCell>{node.data_source}</TableCell>
            <TableCell>{node.is_active ? "Yes" : "No"}</TableCell>
          </TableRow>
        ))}
        {loading && (
          <TableRow>
            <TableCell colSpan={99}>
              <Loading />
            </TableCell>
          </TableRow>
        )}
        {nodes.length === 0 && !loading && (
          <TableRow>
            <TableCell colSpan={99} sx={{ textAlign: "center", py: 10 }}>
              <Typography>No nodes found</Typography>
            </TableCell>
          </TableRow>
        )}
      </TableBody>
    </Table>
  )
}

export default NodesTable
